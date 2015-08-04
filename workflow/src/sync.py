#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.actions import PROJECTS_CACHE_KEY, \
    build_bamboo_facade, PLANS_CACHE_KEY, STATUS_CACHE_KEY, UPDATE_INTERVAL_PROJECTS, UPDATE_INTERVAL_PLANS, \
    UPDATE_INTERVAL_STATUS
from src.util import workflow


def _fetch_bamboo_data_if_necessary(bamboo_facade):
    # cached_data can only take a bare callable (no args),
    # so we need to wrap callables needing arguments in a function
    # that needs none.
    def wrapper_projects():
        return bamboo_facade.projects()

    projects = workflow().cached_data(PROJECTS_CACHE_KEY, wrapper_projects, max_age=UPDATE_INTERVAL_PROJECTS)
    workflow().logger.debug('{} projects cached'.format(len(projects)))

    def wrapper_plans():
        plans_with_branches = bamboo_facade.plans()
        for plan in plans_with_branches:
            branches = bamboo_facade.branches(plan.plan_key)
            plan.branches = branches
        return plans_with_branches

    plans = workflow().cached_data(PLANS_CACHE_KEY, wrapper_plans, max_age=UPDATE_INTERVAL_PLANS)
    workflow().logger.debug('{} plans cached'.format(len(plans)))

    def wrapper_status():
        return bamboo_facade.status()

    status = workflow().cached_data(STATUS_CACHE_KEY, wrapper_status, max_age=UPDATE_INTERVAL_STATUS)
    workflow().logger.debug('{} build results cached'.format(len(status)))


def main(wf):
    bamboo_facade = build_bamboo_facade()
    _fetch_bamboo_data_if_necessary(bamboo_facade)


if __name__ == '__main__':
    workflow().run(main)
