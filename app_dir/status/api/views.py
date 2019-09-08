from rest_framework import mixins
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView)

from .serializers import StatusSerializer, Status
from app_dir.accounts.api.permissions import IsOwnerOrReadOnly


class StatusListAPIView(mixins.CreateModelMixin, ListAPIView):
    serializer_class = StatusSerializer

    def get_queryset(self):
        qs = Status.objects.all()
        query = self.request.GET.get('q')
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class StatusCreateAPIView(CreateAPIView):
    serializer_class = StatusSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Status.objects.all()

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class DetailAPIView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, RetrieveAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsOwnerOrReadOnly]

    # lookup_field = 'id'

    # def get_object(self):
    #     print(self.kwargs)
    #     return Status.objects.get(id=2)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class StatusDeleteAPIView(DestroyAPIView):
    queryset = Status.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = StatusSerializer


class StatusUpdateAPIView(RetrieveUpdateAPIView):
    # permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
