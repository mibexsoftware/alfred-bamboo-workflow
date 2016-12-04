# -*- coding: utf-8 -*-
from src import icons
from src.actions import BambooWorkflowAction
from src.util import workflow


class IndexWorkflowAction(BambooWorkflowAction):
    def menu(self, args):
        workflow().add_item(
            'Bamboo dashboard',
            'See the status of queued and running builds and your build agents',
            autocomplete=':dashboard ',
            icon=icons.STATUS
        )
        workflow().add_item(
            'Search for Bamboo projects',
            'Search for projects and open the project in your browser',
            autocomplete=':projects ',
            icon=icons.PROJECTS
        )
        workflow().add_item(
            'Search for Bamboo plans',
            'Search for plans, browse the plan branches and open or trigger them',
            autocomplete=':plans ',
            icon=icons.PLANS
        )
        workflow().add_item(
            'Bamboo build results',
            'Get the build results of your plans, download artifacts or trigger a rebuild',
            autocomplete=':results ',
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
