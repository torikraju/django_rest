from rest_framework import serializers

from app_dir.status.models import Status
from app_dir.accounts.api.serializers import UserPublicSerializer


class StatusSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)

    class Meta:
        model = Status
        fields = [
            'id',
            'user',
            'content',
            'image'
        ]
        read_only_fields = ['user']

    @staticmethod
    def validate_content(attrs):
        if len(attrs) < 10:
            raise serializers.ValidationError('Too Small')
        return attrs
