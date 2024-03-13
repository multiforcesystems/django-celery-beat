"""Django Application signals."""
from django_celery_beat.schedulers import ModelEntry as Entry
from celery import current_app
from redbeat import RedBeatSchedulerEntry


def redbeat_sync(sender, instance, **kwargs):
    e = Entry(instance, app=current_app)
    r = RedBeatSchedulerEntry(
        name=e.name, task=e.task, schedule=e.schedule, args=e.args, kwargs=e.kwargs, app=e.app,
        options=e.options, total_run_count=e.total_run_count, last_run_at=e.last_run_at, enabled=e.model.enabled)
    print(r.save())


def signals_connect():
    """Connect to signals."""
    from django.db.models import signals

    from .models import (ClockedSchedule, CrontabSchedule, IntervalSchedule,
                         PeriodicTask, PeriodicTasks, SolarSchedule)

    signals.pre_save.connect(
        PeriodicTasks.changed, sender=PeriodicTask
    )
    signals.pre_delete.connect(
        PeriodicTasks.changed, sender=PeriodicTask
    )

    signals.post_save.connect(
        PeriodicTasks.update_changed, sender=IntervalSchedule
    )
    signals.pre_delete.connect(
        PeriodicTasks.update_changed, sender=IntervalSchedule
    )

    signals.post_save.connect(
        PeriodicTasks.update_changed, sender=CrontabSchedule
    )
    signals.post_delete.connect(
        PeriodicTasks.update_changed, sender=CrontabSchedule
    )

    signals.post_save.connect(
        PeriodicTasks.update_changed, sender=SolarSchedule
    )
    signals.post_delete.connect(
        PeriodicTasks.update_changed, sender=SolarSchedule
    )

    signals.post_save.connect(
        PeriodicTasks.update_changed, sender=ClockedSchedule
    )
    signals.post_delete.connect(
        PeriodicTasks.update_changed, sender=ClockedSchedule
    )

    signals.post_save.connect(
        redbeat_sync, sender=PeriodicTask
    )
