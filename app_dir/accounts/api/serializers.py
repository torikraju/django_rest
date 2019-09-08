from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from django.utils import timezone
from datetime import timedelta

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
expire_delta = api_settings.JWT_REFRESH_EXPIRATION_DELTA


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    token = serializers.SerializerMethodField(read_only=True)
    expires = serializers.SerializerMethodField(read_only=True)
    token_response = serializers.SerializerMethodField(read_only=True)
    message = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2',
            'token',
            'expires',
            'token_response',
            'message'
        ]
        # extra_kwargs = {'password': {'write_only': True}}

    def get_message(self, obj):
        return 'Thank you for your registration'

    def get_token_response(self, obj):
        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        context = self.context
        response = jwt_response_payload_handler(token, obj, request=context['request'])
        return response

    def get_token(self, obj):
        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def get_expires(self, obj):
        return timezone.now() + expire_delta - timedelta(seconds=200)

    def validate(self, attrs):
        pw = attrs.get('password')
        pw2 = attrs.pop('password2')
        if pw != pw2:
            raise serializers.ValidationError("password didn't match")
        return attrs

    def validate_email(self, data):
        qs = User.objects.filter(email__iexact=data)
        if qs.exists():
            raise serializers.ValidationError('User with this email already exists')
        return data

    def validate_username(self, data):
        qs = User.objects.filter(username__iexact=data)
        if qs.exists():
            raise serializers.ValidationError('User with this username already exists')
        return data

    def create(self, validated_data):
        user_obj = User(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
        )
        user_obj.set_password(validated_data.get('password'))
        user_obj.save()
        return user_obj
