#!/usr/bin/env python

from sample.app import create_app, celery
from sample import tasks   # noqa


def run_celery():
    app = create_app()
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask

run_celery()
