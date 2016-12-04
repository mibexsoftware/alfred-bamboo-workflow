# -*- coding: utf-8 -*-
from src.actions import BambooFilterableMenu, HOST_URL, PLANS_CACHE_KEY, UPDATE_INTERVAL_PLANS, \
    BambooWorkflowAction, build_bamboo_facade
from src.util import workflow


class BranchesFilterableMenu(BambooFilterableMenu):
    def __init__(self, args):
        super(BranchesFilterableMenu, self).__init__(entity_name='plan branch',
                                                     update_interval=UPDATE_INTERVAL_PLANS,
                                                     cache_key=PLANS_CACHE_KEY,
                                                     args=args)

    def _add_to_result_list(self, branch):
        workflow().add_item(title=branch.name,
                            subtitle=branch.description,
                            largetext=branch.name,
                            arg=':branches ' + branch.key,
                            modifier_subtitles={
                                u'shift': u'Trigger build execution for this plan branch'
                            },  # `cmd``, ``ctrl``, ``shift``, ``alt`` and ``fn``
                            copytext='{}/browse/{}'.format(workflow().settings.get(HOST_URL), branch.key),
                            valid=True)

    def _get_result_filter(self):
        return lambda b: u' '.join([b.name, b.description])

    def _transform_from_cache(self, plans, q):
        return self.__find_branches_matching_plan(plans, q)

    def __find_branches_matching_plan(self, plans, q):
        branches = next((p.branches for p in plans if p.plan_key == q), [])
        return branches

    # args: [':branches', 'plan_key, branch_name]
    def _get_query(self):
        return self.args[-2] if len(self.args) == 3 else self.args[-1]

    def _get_sub_query(self):
        return self.args[-1] if len(self.args) == 3 else None


class BranchesWorkflowAction(BambooWorkflowAction):
    def menu(self, args):
        branch_workflow = BranchesFilterableMenu(args)
        return branch_workflow.run()

    def execute(self, args, ctrl_pressed, shift_pressed):
        branch_key = args[-1]
        if shift_pressed:
            try:
                facade = build_bamboo_facade()
                facade.trigger_build(branch_key)
                print('Successfully triggered build for {}'.format(branch_key))
            except Exception, e:
                print('Failed to trigger build for {}: {}'.format(branch_key, str(e)))
        else:
            import webbrowser
            branch_browse_url = '{}/browse/{}'.format(workflow().settings.get(HOST_URL), branch_key)
            webbrowser.open(branch_browse_url)
