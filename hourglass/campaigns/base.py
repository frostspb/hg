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

    class Meta:
        abstract = True

    @transition(field='state', source=[States.STATE_NEW, States.STATE_PAUSE], target=States.STATE_RUNNING)
    def start(self):
        pass

    @transition(field='state', source=States.STATE_RUNNING, target=States.STATE_PAUSE)
    def pause(self):
        pass

    @transition(field='state', source=[States.STATE_RUNNING, States.STATE_PAUSE], target=States.STATE_STOPPED)
    def stop(self):
        pass

    @transition(field='state', source=States.STATE_PAUSE, target=States.STATE_RUNNING)
    def resume(self):
        pass


class BaseReportPercentItem(BaseStateItem):
    percent = models.FloatField
    name = models.CharField(max_length=256)

    class Meta:
        abstract = True
