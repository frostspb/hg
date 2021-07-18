from datetime import timedelta
from django.db import models

from django.utils.timezone import now
from django_extensions.db.models import TimeStampedModel
from django_fsm import FSMField, transition

from django.core.validators import MaxValueValidator, MinValueValidator
from hourglass.clients.models import Client
from hourglass.contrib.mixins import StateMixin


class BaseStateItem(TimeStampedModel):
    class States:
        STATE_RUNNING = 'running'
        STATE_PAUSE = 'pause'

        STATE_CHOICES = (
            (STATE_RUNNING, STATE_RUNNING),
            (STATE_PAUSE, STATE_PAUSE),

        )
    state = FSMField("Status", default=StateMixin.States.STATE_RUNNING, choices=StateMixin.States.STATE_CHOICES)
    started_at = models.DateTimeField(null=True, blank=True)
    execution_time = models.IntegerField(default=0)

    class Meta:
        abstract = True

    @property
    def duration(self):
        if self.state == self.States.STATE_RUNNING and self.started_at:
            return self.execution_time + (now() - self.started_at).minutes
        else:
            return self.execution_time

    @transition(field='state', source=States.STATE_PAUSE, target=States.STATE_RUNNING)
    def start(self):
        self.started_at = now()

    @transition(field='state', source=States.STATE_RUNNING, target=States.STATE_PAUSE)
    def pause(self):
        self.execution_time += (now() - self.started_at).minutes
        self.started_at = None


class BaseReportPercentItem(BaseStateItem):
    percent = models.FloatField(default=0, validators=[MaxValueValidator(100)])
    name = models.CharField(max_length=256)

    class Meta:
        abstract = True
