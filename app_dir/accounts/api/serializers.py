from rest_framework import serializers
from django.contrib.auth.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2'
        ]
        # extra_kwargs = {'password': {'write_only': True}}

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

    def validate_username(self, data):
        qs = User.objects.filter(username__iexact=data)
        if qs.exists():
            raise serializers.ValidationError('User with this username already exists')

    def create(self, validated_data):
        user_obj = User(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
        )
        user_obj.set_password(validated_data.get('password'))
        user_obj.save()
        return user_obj
