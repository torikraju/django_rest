from django.contrib.auth.models import User
from django.db import models


def upload_status_image(instance, filename):
    return f'updates/{instance.user}/{filename}'


class Status(models.Model):
    user = models.ForeignKey(User, default='', on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=upload_status_image, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.username)

    class Meta:
        verbose_name = 'Status Post'
        verbose_name_plural = 'Status Post'

    @property
    def owner(self):
        return self.user
