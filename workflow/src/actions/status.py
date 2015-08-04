# -*- coding: utf-8 -*-
from src.actions import HOST_URL, build_bamboo_facade, STATUS_CACHE_KEY, get_data_from_cache, \
    BambooFilterableMenu, UPDATE_INTERVAL_STATUS, BambooWorkflowAction
from src import icons
from src.util import workflow, strip_tags


class StatusFilterableMenu(BambooFilterableMenu):
    def __init__(self, args):
        super(StatusFilterableMenu, self).__init__(entity_name='build results',
                                                   update_interval=UPDATE_INTERVAL_STATUS,
                                                   cache_key=STATUS_CACHE_KEY,
                                                   args=args)

    def _add_to_result_list(self, build_result):
        build_result_info = u'{} / #{}'.format(build_result.plan_name, str(build_result.build_number))
        workflow().add_item(title=build_result_info,
                            icon=self._icon_for_build_status(build_result.build_state),
                            subtitle=u'{}, duration: {}, {}, {}'.format(build_result.test_summary,
                                                                        build_result.duration_desc,
                                                                        build_result.relative_time,
                                                                        strip_tags(build_result.build_reason)),
                            modifier_subtitles={
                                u'cmd': u'Open page of artifacts to download',
                                u'shift': u'Trigger build execution for this plan'
                            },  # `cmd``, ``ctrl``, ``shift``, ``alt`` and ``fn``
                            largetext=build_result_info,
                            arg=':status {} {}'.format(build_result.build_result_key, build_result.plan_key),
                            copytext='{}/browse/{}'.format(workflow().settings.get(HOST_URL),
                                                           build_result.build_result_key),
                            valid=True)

    def _icon_for_build_status(self, build_state):
        if build_state == 'Successful':
            return icons.BUILD_SUCCESS
        elif build_state == 'Failed':
            return icons.BUILD_FAILED
        else:
            return icons.BUILD_UNKNOWN

    def _get_result_filter(self):
        return lambda br: u' '.join([br.plan_name, str(br.build_number), br.build_result_key])

    def _transform_from_cache(self, build_results, q):
        return sorted(build_results, key=lambda br: br.is_failed(), reverse=True) if build_results else []


class StatusWorkflowAction(BambooWorkflowAction):
    def menu(self, args):
        status_workflow = StatusFilterableMenu(args)
        return status_workflow.run()

    def execute(self, args, cmd_pressed, shift_pressed):
        import webbrowser
        build_result_key, plan_key = args[-2], args[-1]

        if cmd_pressed:
            build_results = get_data_from_cache(STATUS_CACHE_KEY, UPDATE_INTERVAL_STATUS)
            build_result = next((br for br in build_results if br.build_result_key == build_result_key), None)
            webbrowser.open(build_result.artifact_href)
        elif shift_pressed:
            try:
                facade = build_bamboo_facade()
                facade.trigger_build(plan_key)
                print('Successfully triggered build for {}'.format(build_result_key))
            except Exception, e:
                print('Failed to trigger build for {}: {}'.format(build_result_key, str(e)))
        else:
            build_result_rul = '{}/browse/{}'.format(workflow().settings.get(HOST_URL), build_result_key)
            webbrowser.open(build_result_rul)
