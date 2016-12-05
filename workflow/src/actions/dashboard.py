# -*- coding: utf-8 -*-

from src import icons
from src.actions import HOST_URL, BambooWorkflowAction
from src.util import workflow


class DashboardWorkflowAction(BambooWorkflowAction):
    def menu(self, args):
        from src.actions import build_bamboo_facade
        bamboo_facade = build_bamboo_facade()
        dashboard = bamboo_facade.dashboard()
        workflow().add_item(title=dashboard.agent_summary,
                            largetext=dashboard.agent_summary,
                            arg=':dashboard viewAgents',
                            icon=self._icon_for_overall_status(dashboard.status),
                            valid=True)
        for q in dashboard.builds:
            try:
                agent_name = 'on {}'.format(q['agent']['name']) if 'agent' in q else ''
                workflow().add_item(title='{}: {}'.format(q['planName'], q['jobName']),
                                    subtitle='{}: {} {}'.format(q['messageType'], q['messageText'], agent_name),
                                    largetext=q['messageType'],
                                    icon=self._icon_for_build_status(q['messageType']),
                                    arg=':dashboard {}'.format(q['resultKey']),
                                    modifier_subtitles={u'shift': u'Stop currently running build'},
                                    # `cmd``, ``ctrl``, ``shift``, ``alt`` and ``fn``
                                    valid=True)
            except:
                # sometimes the build results JSON does not contain proper build items
                pass

        workflow().add_item('Main menu', autocomplete='', icon=icons.GO_BACK)

    def _icon_for_build_status(self, build_state):
        if build_state == 'PROGRESS':
            return icons.SYNC
        elif build_state == 'ERROR':
            return icons.BUILD_FAILED
        else:
            return icons.BUILD_UNKNOWN

    def _icon_for_overall_status(self, overall_status):
        if overall_status == 'OK':
            return icons.BUILD_SUCCESS
        elif overall_status == 'ERROR':
            return icons.BUILD_FAILED
        else:
            return icons.BUILD_UNKNOWN

    def execute(self, args, ctrl_pressed, shift_pressed):
        import webbrowser
        host_url = workflow().settings.get(HOST_URL)
        if args[-1] == 'viewAgents':
            webbrowser.open('{}/admin/agent/viewAgents.action'.format(host_url))
        elif shift_pressed:
            from src.actions import build_bamboo_facade
            bamboo_facade = build_bamboo_facade()
            try:
                bamboo_facade.stop_build(args[-1])
                print('Successfully stopped build for {}'.format(args[-1]))
            except Exception, e:
                workflow().logger.debug('workflow ' + str(e))
                print('Failed to stop build for {}: {}'.format(args[-1], str(e)))
        else:
            webbrowser.open('{}/browse/{}'.format(host_url, args[-1]))
