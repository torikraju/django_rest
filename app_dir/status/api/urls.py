from django.urls import path

from .views import (
    StatusListAPIView, StatusCreateAPIView, DetailAPIView, StatusUpdateAPIView,StatusDeleteAPIView
)

urlpatterns = [
    path('', StatusListAPIView.as_view(), name='status-list'),
    path('create', StatusCreateAPIView.as_view(), name='status-creator'),
    path('details/<int:pk>/', DetailAPIView.as_view(), name='status-details'),
    path('delete/<int:pk>/', StatusDeleteAPIView.as_view(), name='status-destroyer'),
    path('update/<int:pk>/', StatusUpdateAPIView.as_view(), name='status-updater')
]
