from django.conf import settings
from rest_framework_jwt.views import refresh_jwt_token
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token
from .views import AuthView

urlpatterns = [
    path('', AuthView.as_view()),
    path('api-token-auth', obtain_jwt_token),
    path('api-token-refresh', refresh_jwt_token),
]
