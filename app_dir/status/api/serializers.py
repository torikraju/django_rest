from rest_framework import serializers

from app_dir.status.models import Status


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

    def validate_content(self, attrs):
        if len(attrs) < 10:
            raise serializers.ValidationError('Too Small')
        return attrs
