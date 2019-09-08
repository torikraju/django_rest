from rest_framework import permissions
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings
from .utils import jwt_response_payload_handler
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


class AuthView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({'details': 'You are already authenticated'})
        data = self.request.data
        username = data.get('username')
        password = data.get('password')
        # user = authenticate(username=username, password=password)
        qs = User.objects.filter(
            Q(username__iexact=username) |
            Q(email__iexact=username)
        )
        if qs.count() == 1:
            user_obj = qs.first()
            if user_obj.check_password(password):
                user = user_obj
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                response = jwt_response_payload_handler(token, user, request=request)
                return Response(response)
        return Response({'details': 'Invalid username or password'}, status=401)
