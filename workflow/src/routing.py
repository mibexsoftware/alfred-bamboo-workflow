# -*- coding: utf-8 -*-
from src.actions import notify_if_upgrade_available, HOST_URL
from src.actions.branches import BranchesWorkflowAction
from src.actions.configure import ConfigureWorkflowAction
from src.actions.help import HelpWorkflowAction
from src.actions.index import IndexWorkflowAction
from src.actions.plans import PlanWorkflowAction
from src.actions.projects import ProjectWorkflowAction
from src.actions.status import StatusWorkflowAction
from src.util import workflow, call_alfred

WORKFLOW_ACTIONS = {
    ':config':   ConfigureWorkflowAction,
    ':projects': ProjectWorkflowAction,
    ':plans':    PlanWorkflowAction,
    ':branches': BranchesWorkflowAction,
    ':status':   StatusWorkflowAction,
    ':help':     HelpWorkflowAction
}

def route(args):  # e.g., args = ":config sethost http://localhost,--exec"
    command_string = args[0]  # :config sethost http://localhost
    command = command_string.split(' ')

    if not workflow().settings.get(HOST_URL, None) and 'sethost' not in command:
        call_alfred('bamboo:config sethost ')
        return

    handler = IndexWorkflowAction
    action = next(iter(command), None)
    if action:
        handler = WORKFLOW_ACTIONS.get(action, IndexWorkflowAction)

    if '--exec' in args:
        handler().execute(command, cmd_pressed='--cmd' in args, shift_pressed='--shift' in args)
    else:  # show menu
        handler().menu(command)
        notify_if_upgrade_available()
        workflow().send_feedback()
