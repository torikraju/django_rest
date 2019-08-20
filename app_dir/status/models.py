from django.contrib.auth.models import User
from django.db import models


class Status(models.Model):
    user = models.ForeignKey(User, default='', on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    # image = models.i
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.username)

    class Meta:
        verbose_name = 'Status Post'
        verbose_name_plural = 'Status Post'
