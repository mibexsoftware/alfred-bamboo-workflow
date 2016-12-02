# -*- coding: utf-8 -*-
from src.actions import HOST_URL, USER_NAME, USER_PW, VERIFY_CERT, update_bamboo_cache, \
    BambooWorkflowAction
from src import icons
from src.lib.workflow import PasswordNotFound
from src.util import workflow, call_alfred
from src.actions import try_bamboo_connection


class ConfigureWorkflowAction(BambooWorkflowAction):

    def menu(self, args):
        if 'sethost' in args:
            workflow().add_item(
                'Type a new Bamboo host URL',
                'Enter the full URL to your Bamboo host, e.g. http://10.0.0.1/bamboo',
                valid=True, arg=' '.join(args), icon=icons.HOST
            )
            if workflow().settings.get(HOST_URL, None):
                _add_cancel_workflow_action()
        elif 'setuser' in args:
            workflow().add_item(
                'Type a new Bamboo username',
                'Enter the name of the Bamboo user which you would like to use to connect',
                valid=True, arg=' '.join(args), icon=icons.USER
            )
            _add_cancel_workflow_action()
        elif 'setpw' in args:
            workflow().add_item(
                'Type a new Bamboo password',
                'Enter the password of the Bamboo user. It will be stored encrypted in Keychain.',
                valid=True, arg=' '.join(args), icon=icons.PASSWORD
            )
            _add_cancel_workflow_action()
        elif 'check' in args:
            try_bamboo_connection()
            _add_cancel_workflow_action()
        else:
            workflow().add_item(
                'Bamboo host URL',
                workflow().settings.get(HOST_URL, 'Not configured'),
                autocomplete=':config sethost ', icon=icons.HOST
            )
            workflow().add_item(
                'Bamboo user name',
                workflow().settings.get(USER_NAME, 'Not configured'),
                autocomplete=':config setuser ', icon=icons.USER
            )
            try:
                pw = workflow().get_password(USER_PW)
                bamboo_pw = '******' if pw else 'Not configured'
            except PasswordNotFound:
                bamboo_pw = 'Not configured'

            workflow().add_item(
                'Bamboo user password',
                'Current password: {}'.format(bamboo_pw),
                autocomplete=':config setpw ', icon=icons.PASSWORD
            )
            verify_cert = 'Enabled' if workflow().settings.get(VERIFY_CERT, 'false') == 'true' else 'Disabled'
            workflow().add_item(
                'Validate certificate when accessing Bamboo over HTTPS',
                verify_cert,
                arg=':config verifycert', valid=True, icon=icons.CERT
            )
            workflow().add_item(
                'Check connection to Bamboo',
                'Checks if a Bamboo connection can be established with the given configuration.',
                autocomplete=':config check ', icon=icons.CHECK
            )
            workflow().add_item(
                'Sync Bamboo data cache',
                'Deletes the cache of Bamboo data and triggers a new synchronization in the background.',
                arg=':config sync', valid=True, icon=icons.SYNC
            )
            workflow().add_item(
                'Update workflow',
                'Updates the workflow to the latest version (will be checked automatically periodically).',
                arg=':config update', valid=True, icon=icons.UPDATE
            )
            workflow().add_item(
                'Switch theme',
                'Toggle between light and dark icons',
                arg = ':config switchtheme', valid = True, icon = icons.SWITCH_THEME
            )
            workflow().add_item('Main menu', autocomplete='', icon=icons.GO_BACK)

    def execute(self, args, cmd_pressed, shift_pressed):
        if 'sethost' in args:
            workflow().settings[HOST_URL] = args[-1]
            print('New Bamboo host: {}'.format(args[-1]))
        elif 'setuser' in args:
            workflow().settings[USER_NAME] = args[-1]
            print('New Bamboo user: {}'.format(args[-1]))
        elif 'setpw' in args:
            workflow().save_password(USER_PW, args[-1])
            print('Saved Bamboo password in keychain')
        elif 'verifycert' in args:
            verify_cert = workflow().settings.get(VERIFY_CERT, 'false') == 'true'
            toggle = (str(not verify_cert)).lower()
            workflow().settings[VERIFY_CERT] = toggle
            print('Enabled certificate verification' if toggle == 'true' else 'Disabled certificate verification')
        elif 'sync' in args:
            workflow().clear_cache()
            update_bamboo_cache()
            print('Bamboo data synchronization triggered')
        elif 'update' in args:
            try:
                if workflow().start_update():
                    print('Update of workflow finished')
                else:
                    print('You already have the latest workflow version')
            except Exception, e:
                print('Update of workflow failed: {}'.format(str(e)))
        elif 'switchtheme' in args:
            icon_theme = 'light' if icons.icon_theme() == 'dark' else 'dark'
            workflow().settings[icons.ICON_THEME] = icon_theme
            print('The workflow is now using the %s icon theme' % icon_theme)

        call_alfred('bamboo:config')


def _add_cancel_workflow_action():
    workflow().add_item('Cancel', autocomplete=':config', icon=icons.GO_BACK)
