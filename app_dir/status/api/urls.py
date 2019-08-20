from django.urls import path

from .views import (
    StatusListAPIView, StatusCreateAPIView, DetailAPIView
)

urlpatterns = [
    path('', StatusListAPIView.as_view(), name='status-list'),
    path('create', StatusCreateAPIView.as_view(), name='status-creator'),
    path('details/<int:id>/', DetailAPIView.as_view(), name='status-details'),
    # path('delete/<int:pk>/', UserDeleteAPIView.as_view(), name='user-destroyer'),
    # path('update/<int:pk>/', UpdateAPIView.as_view(), name='status-updater')
]
