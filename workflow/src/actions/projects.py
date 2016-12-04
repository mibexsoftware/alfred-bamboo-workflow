# -*- coding: utf-8 -*-
from src.actions import BambooFilterableMenu, HOST_URL, PROJECTS_CACHE_KEY, \
    UPDATE_INTERVAL_PROJECTS, BambooWorkflowAction
from src.util import workflow


class ProjectsFilterableMenu(BambooFilterableMenu):
    def __init__(self, args):
        super(ProjectsFilterableMenu, self).__init__(entity_name='projects',
                                                     update_interval=UPDATE_INTERVAL_PROJECTS,
                                                     cache_key=PROJECTS_CACHE_KEY,
                                                     args=args)

    def _add_to_result_list(self, project):
        workflow().add_item(title=project.name,
                            largetext=project.name,
                            arg=':projects {}'.format(project.key),
                            copytext='{}/browse/{}'.format(workflow().settings.get(HOST_URL), project.key),
                            valid=True)

    def _get_result_filter(self):
        return lambda p: u' '.join([p.name])


class ProjectWorkflowAction(BambooWorkflowAction):
    def menu(self, args):
        project_workflow = ProjectsFilterableMenu(args)
        return project_workflow.run()

    def execute(self, args, ctrl_pressed, shift_pressed):
        import webbrowser
        project_key = args[-1]
        project_browse_url = '{}/browse/{}'.format(workflow().settings.get(HOST_URL), project_key)
        webbrowser.open(project_browse_url)
