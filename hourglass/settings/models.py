import random
#
from django.db import models
from solo.models import SingletonModel


class HourglassSettings(SingletonModel):
    base_campaigns_count = models.SmallIntegerField("Base count", default=100)
    min_delta_val = models.SmallIntegerField("Min delta value", default=3)
    max_delta_val = models.SmallIntegerField("Max delta value", default=5)

    def get_value(self):
        delta = random.randint(self.min_delta_val, self.max_delta_val)
        seed = random.randint(0, 10)
        if seed > 5:
            value = self.base_campaigns_count - delta
        else:
            value = self.base_campaigns_count + delta
        return value