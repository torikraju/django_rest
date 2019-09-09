from rest_framework import serializers

from app_dir.status.models import Status
from app_dir.accounts.api.serializers import UserPublicSerializer


class StatusSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    user_uri = serializers.HyperlinkedRelatedField(
        source='user',
        lookup_field='username',
        view_name='auth_api:user-details',
        read_only=True
    )
    email = serializers.SlugRelatedField(
        source='user',
        read_only=True,
        slug_field='email'
    )

    class Meta:
        model = Status
        fields = [
            'id',
            'user',
            'content',
            'image',
            'user_uri',
            'email'
        ]
        read_only_fields = ['user']

    @staticmethod
    def validate_content(attrs):
        if len(attrs) < 10:
            raise serializers.ValidationError('Too Small')
        return attrs
