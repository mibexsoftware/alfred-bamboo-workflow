# -*- coding: utf-8 -*-
from src import icons
from src.actions import BambooWorkflowAction
from src.util import workflow


class IndexWorkflowAction(BambooWorkflowAction):
    def menu(self, args):
        workflow().add_item(
            'Search for Bamboo projects',
            'Search for projects and open the project page in your default browser',
            autocomplete=':projects ',
            icon=icons.PROJECTS
        )
        workflow().add_item(
            'Search for Bamboo plans',
            'Search for plans, go to your plan branches and open them in your default browser',
            autocomplete=':plans ',
            icon=icons.PLANS
        )
        workflow().add_item(
            'Bamboo Build status',
            'Get the build status of your plans, download artifacts or trigger a rebuild',
            autocomplete=':status ',
            icon=icons.STATUS
        )
        workflow().add_item(
            'Preferences',
            'Change Bamboo connection settings, refresh the cache or the workflow itself',
            autocomplete=':config ',
            icon=icons.SETTINGS
        )
        workflow().add_item(
            'Help',
            'Get help about the workflow and how to get support',
            autocomplete=':help ',
            icon=icons.HELP
        )
