from django.contrib import admin

from .forms import StatusForm
from .models import Status


class StatusAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at']

    form = StatusForm

    class Meta:
        model = Status


admin.site.register(Status, StatusAdmin)
