# -*- coding: utf-8 -*-
from src.bamboo.branch import Branch
from src.bamboo.build_result import BuildResult
from src.bamboo.dashboard import DashBoard
from src.bamboo.plan import Plan
from src.bamboo.project import Project
from src.bamboo.trigger_result import TriggerResult

from src.lib import requests
from src.lib import iso8601

# We use requests library for HTTP connections because workflow.web does not verify SSL certificates!
# see http://www.deanishe.net/alfred-workflow/api/web.html


class BambooFacade(object):
    JSON_HEADER = {'Accept': 'application/json'}  # this is necessary as Bamboo supports both XML and json
    BAMBOO_API_VERSION = 'latest'

    def __init__(self, bamboo_host, bamboo_user=None, bamboo_pw=None, verify=True):
        super(BambooFacade, self).__init__()
        self._bamboo_user = bamboo_user
        self._bamboo_pw = bamboo_pw
        self._verify = verify
        if bamboo_host.endswith("/"):
            self._base_url = bamboo_host[:-1]
        else:
            self._base_url = bamboo_host
        self._bamboo_api_base = '{}/rest/api/{}'.format(self._base_url, self.BAMBOO_API_VERSION)

    def projects(self):
        return [Project.from_json(json)
                for json in self._page(url=self._bamboo_url('/project'),
                                       params={'max-result': 100},
                                       result_name='project', prefix='projects')]

    def plans(self):
        return [Plan.from_json(json)
                for json in self._page(url=self._bamboo_url('/plan'),
                                       params={'expand': 'plans.plan', 'max-result': 100},
                                       result_name='plan', prefix='plans')]

    def branches(self, plan_key):
        return [Branch.from_json(json, plan_key)
                # using /search/branches instead of /plan/{projectKey}-{buildKey}/branch has the advantage that we
                # get the master branch as well (but we cannot filter out deactivated plan branches unfortunately)
                for json in self._page(url=self._bamboo_url('/search/branches'),
                                       params={'masterPlanKey': plan_key,
                                               'includeMasterBranch': 'true',
                                               'max-result': 100},
                                       result_name='searchResults')]

    def results(self):
        build_results = [BuildResult.from_json(json) for json in self._page(url=self._bamboo_url('/result'),
                                                                            params={
                                                                                'expand': 'results.result.artifacts',
                                                                                'max-result': 100
                                                                            },
                                                                            result_name='result',
                                                                            prefix='results')]
        build_results.sort(key=lambda x: iso8601.parse_date(x.completed_date), reverse=True)
        return build_results

    def dashboard(self):
        json = self._get('{}/build/admin/ajax/getDashboardSummary.action'.format(self._base_url), params={})
        dashboard = DashBoard.from_json(json)
        return dashboard

    def stop_build(self, plan_result_key):
        self._delete(self._bamboo_url('/queue/{}'.format(plan_result_key)),
                     params={'stage': '', 'executeAllStages': 'true'})

    def is_running(self):
        # we have to use /info instead of /server because the latter does not need authentication which would not
        # allow us to verify if the Bamboo credentials are ok
        json = self._get(self._bamboo_url('/info'), params={})
        return json['state'] == 'RUNNING'

    def trigger_build(self, build_key):
        json = self._post(self._bamboo_url('/queue/{}'.format(build_key)), params={'executeAllStages': 'true'})
        return TriggerResult.from_json(json)

    def _bamboo_url(self, resource_path):
        return self._url(self._bamboo_api_base, resource_path)

    def _url(self, api_base, resource_path):
        if not resource_path.startswith("/"):
            resource_path = "/" + resource_path
        return api_base + resource_path

    def _get(self, url, params):
        response = requests.get(url, params=params, headers=self.JSON_HEADER, **(self._http_options()))
        return self.__get_json_response(response)

    def _post(self, url, params):
        response = requests.post(url, params=params, headers=self.JSON_HEADER, **(self._http_options()))
        return self.__get_json_response(response)

    def _delete(self, url, params):
        requests.delete(url, params=params, headers=self.JSON_HEADER, **(self._http_options()))

    def __get_json_response(self, response):
        response.raise_for_status()
        return response.json()

    def _http_options(self):
        return {
            'auth': self._get_credentials(),
            'verify': self._verify
        }

    def _get_credentials(self):
        if self._bamboo_user is not None:
            credentials = (self._bamboo_user, self._bamboo_pw)
        else:
            credentials = None
        return credentials

    def _page(self, url, params, result_name, prefix=None):
        has_more = True
        start = None

        while has_more:
            if start is not None:
                params['start-index'] = start

            json = self._get(url, params)
            if prefix:
                json = json[prefix]

            for item in json[result_name]:
                yield item

            has_more = json['start-index'] != 0
            if has_more:
                start = json['start-index']
