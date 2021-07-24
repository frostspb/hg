from django.contrib import admin
from solo.admin import SingletonModelAdmin

from .models import HourglassSettings


@admin.register(HourglassSettings)
class SettingsAdmin(SingletonModelAdmin):
    list_display = ["base_campaigns_count", "min_delta_val", "max_delta_val"]
    search_fields = ["name", "id"]
    fields = ["base_campaigns_count", "min_delta_val", "max_delta_val", ]
