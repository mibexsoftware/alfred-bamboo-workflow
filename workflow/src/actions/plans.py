# -*- coding: utf-8 -*-

from src.actions import BambooFilterableMenu, PLANS_CACHE_KEY, UPDATE_INTERVAL_PLANS, HOST_URL, BambooWorkflowAction, \
    build_bamboo_facade
from src.util import workflow, call_alfred

FAVOURITE_PLAN = u'★'


class PlansFilterableMenu(BambooFilterableMenu):
    def __init__(self, args):
        super(PlansFilterableMenu, self).__init__(entity_name='plans',
                                                  update_interval=UPDATE_INTERVAL_PLANS,
                                                  cache_key=PLANS_CACHE_KEY,
                                                  args=args)

    def _add_to_result_list(self, plan):
        workflow().add_item(title=u'{} {}'.format(plan.name, FAVOURITE_PLAN if plan.is_favourite else ''),
                            subtitle=plan.description,
                            largetext=plan.name,
                            arg=':plans ' + plan.plan_key,
                            modifier_subtitles={
                                u'shift': u'Trigger build execution for this plan'
                            },  # `cmd``, ``ctrl``, ``shift``, ``alt`` and ``fn``
                            copytext='{}/browse/{}'.format(workflow().settings.get(HOST_URL), plan.plan_key),
                            valid=True)

    def _get_result_filter(self):
        return lambda p: u' '.join([p.name, p.description])

    def _transform_from_cache(self, plans, q):
        return sorted(plans, key=lambda p: p.is_favourite, reverse=True) if plans else []


class PlanWorkflowAction(BambooWorkflowAction):
    def menu(self, args):
        plan_workflow = PlansFilterableMenu(args)
        return plan_workflow.run()

    def execute(self, args, ctrl_pressed, shift_pressed):
        plan_key = args[-1]
        if shift_pressed:
            try:
                facade = build_bamboo_facade()
                facade.trigger_build(plan_key)
                print('Successfully triggered build for {}'.format(plan_key))
            except Exception, e:
                print('Failed to trigger build for {}: {}'.format(plan_key, str(e)))
        else:
            call_alfred('bamboo:branches {} '.format(plan_key))
