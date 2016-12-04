# -*- coding: utf-8 -*-
from src import icons
from src.lib.requests.exceptions import SSLError

from src.lib.workflow import PasswordNotFound
from src.lib.workflow.background import run_in_background
from src.lib.workflow.background import is_running

from src.bamboo.bamboo_facade import BambooFacade
from src.util import workflow

# How often to check for new / updated Bamboo data
UPDATE_INTERVAL_PROJECTS = 24 * 60 * 60  # every day
UPDATE_INTERVAL_PLANS = 8 * 60 * 60  # every 8 hours
UPDATE_INTERVAL_STATUS = 10 * 60  # every 10 minutes

# By default, Workflow.filter() will match and return anything that contains all the characters in
# query in the same order, regardless of case. So we want to restrict this by using a min score
# see http://alfredworkflow.readthedocs.org/en/latest/user-manual/filtering.html for more information
SEARCH_MIN_SCORE = 20

HOST_URL = 'host_url'
USER_NAME = 'user_name'
USER_PW = 'user_pw'
VERIFY_CERT = 'verify_cert'

PROJECTS_CACHE_KEY = 'projects'
STATUS_CACHE_KEY = 'status'
PLANS_CACHE_KEY = 'plans'

SYNC_JOB_NAME = u'sync'


def build_bamboo_facade():
    bamboo_host = workflow().settings.get(HOST_URL, None)
    if not bamboo_host:
        raise ValueError('Bamboo host URL not set.')
    bamboo_user = workflow().settings.get(USER_NAME, None)
    try:
        bamboo_pw = workflow().get_password(USER_PW)
    except PasswordNotFound:
        bamboo_pw = None
    verify_cert = workflow().settings.get(VERIFY_CERT, 'false') == 'true'
    return BambooFacade(bamboo_host, bamboo_user, bamboo_pw, verify_cert)


def _notify_if_cache_update_in_progress():
    # Notify the user if the cache is being updated
    if is_running(SYNC_JOB_NAME):
        workflow().add_item('Getting data from Bamboo. Please try again in a second or two...',
                            valid=False,
                            icon=icons.INFO)


def try_bamboo_connection(show_success=True):
    try:
        bamboo_facade = build_bamboo_facade()
        bamboo_facade.is_running()
        if show_success:
            workflow().add_item('Congratulations, connection to Bamboo was successful!', icon=icons.OK)
        return True
    except SSLError:
        workflow().add_item('SSL error: Try with certificate verification disabled', icon=icons.ERROR)
        return False
    except Exception, e:
        workflow().add_item('Error when connecting Bamboo server', str(e), icon=icons.ERROR)
        return False


def get_data_from_cache(cache_key, update_interval):
    # Set `data_func` to None, as we don't want to update the cache in this script and `max_age` to 0
    # because we want the cached data regardless of age
    try:
        data = workflow().cached_data(cache_key, None, max_age=0)
    except Exception:
        # this might happen when there are incompatible model changes and the pickle cache cannot be deserialized
        # anymore => in this case it is better to clear the cache and to re-trigger data syncing
        workflow().clear_cache()
        data = []

    # Start update script if cached data is too old (or doesn't exist)
    if not workflow().cached_data_fresh(cache_key, max_age=update_interval):
        update_bamboo_cache()

    return data


def update_bamboo_cache():
    cmd = ['/usr/bin/python', '-msrc.sync']
    run_in_background(SYNC_JOB_NAME, cmd)


class BambooWorkflowAction(object):

    def menu(self, args):
        raise NotImplementedError

    def execute(self, args, cmd_pressed, shift_pressed):
        pass  # not every action can be executed


class BambooFilterableMenu(object):
    def __init__(self, entity_name, args, update_interval, cache_key):
        self.entity_name = entity_name
        self.args = args
        self.update_interval = update_interval
        self.cache_key = cache_key

    def run(self):
        workflow().logger.debug('workflow args: {}'.format(self.args))

        data = get_data_from_cache(self.cache_key, self.update_interval)
        entities = self._transform_from_cache(data, self._get_query())
        _notify_if_cache_update_in_progress()

        query = self._get_sub_query()
        # query may not be empty or contain only whitespace. This will raise a ValueError.
        if query and entities:
            entities = workflow().filter(query, entities, key=self._get_result_filter(), min_score=SEARCH_MIN_SCORE)
            workflow().logger.debug('{} {} matching `{}`'.format(self.entity_name, len(entities), self._get_query()))

        if not entities:
            # only do a REST call in case there is no query given because only in that case it is likely that there
            # is a problem with the connection to Bamboo and we would like to prevent doing slow calls in here
            if query or (not query and try_bamboo_connection(show_success=False)):
                workflow().add_item('No matching {} found.'.format(self.entity_name), icon=icons.ERROR)
        else:
            for e in entities:
                self._add_to_result_list(e)

        self.__add_item_after_last_result()

    def _get_result_filter(self):
        raise NotImplementedError

    def _transform_from_cache(self, entities, query):
        return entities

    def _get_query(self):
        return self.args[-1]

    def _get_sub_query(self):
        return self.args[-1]

    def _add_to_result_list(self, entity):
        raise NotImplementedError

    def __add_item_after_last_result(self):
        workflow().add_item('Main menu', autocomplete='', icon=icons.GO_BACK)
