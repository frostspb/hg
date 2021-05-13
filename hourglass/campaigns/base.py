from datetime import timedelta
from django.db import models

from django.utils.timezone import now
from django_extensions.db.models import TimeStampedModel
from django_fsm import FSMField, transition


from hourglass.clients.models import Client
from hourglass.contrib.mixins import StateMixin


class BaseStateItem(TimeStampedModel):
    class States:
        STATE_NEW = 'new'
        STATE_RUNNING = 'running'
        STATE_PAUSE = 'pause'
        STATE_STOPPED = 'stopped'

        STATE_CHOICES = (
            (STATE_NEW, STATE_NEW),
            (STATE_RUNNING, STATE_RUNNING),
            (STATE_PAUSE, STATE_PAUSE),
            (STATE_STOPPED, STATE_STOPPED),

        )
    state = FSMField(default=StateMixin.States.STATE_NEW, choices=StateMixin.States.STATE_CHOICES)
    started_at = models.DateTimeField(null=True, blank=True)
    execution_time = models.IntegerField(default=0)

    class Meta:
        abstract = True

    @property
    def duration(self):
        if self.state == self.States.STATE_RUNNING:
            return self.execution_time + (now() - self.started_at).seconds
        else:
            return self.execution_time

    @transition(field='state', source=[States.STATE_NEW, States.STATE_PAUSE], target=States.STATE_RUNNING)
    def start(self):
        self.started_at = now()

    @transition(field='state', source=States.STATE_RUNNING, target=States.STATE_PAUSE)
    def pause(self):
        self.execution_time += (now() - self.started_at).seconds
        self.started_at = None

    @transition(field='state', source=[States.STATE_RUNNING, States.STATE_PAUSE], target=States.STATE_STOPPED)
    def stop(self):
        self.execution_time += (now() - self.started_at).seconds
        self.started_at = None

    @transition(field='state', source=States.STATE_PAUSE, target=States.STATE_RUNNING)
    def resume(self):
        self.started_at = now()


class BaseReportPercentItem(BaseStateItem):
    percent = models.FloatField
    name = models.CharField(max_length=256)

    class Meta:
        abstract = True
