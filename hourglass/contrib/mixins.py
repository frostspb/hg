from django_fsm import transition


class StateMixin:
    class States:
        STATE_RUNNING = 'running'
        STATE_PAUSE = 'pause'

        STATE_CHOICES = (

            (STATE_RUNNING, STATE_RUNNING),
            (STATE_PAUSE, STATE_PAUSE),


        )

    @transition(field='state', source=States.STATE_PAUSE, target=States.STATE_RUNNING)
    def start(self):
        pass

    @transition(field='state', source=States.STATE_RUNNING, target=States.STATE_PAUSE)
    def pause(self):
        pass
