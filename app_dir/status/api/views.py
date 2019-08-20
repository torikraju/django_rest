from rest_framework.generics import (
    ListAPIView,
    CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView)

from .serializers import StatusSerializer, Status


class StatusListAPIView(ListAPIView):
    serializer_class = StatusSerializer

    def get_queryset(self):
        qs = Status.objects.all()
        query = self.request.GET.get('q')
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs


class StatusCreateAPIView(CreateAPIView):
    serializer_class = StatusSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Status.objects.all()

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class DetailAPIView(RetrieveAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    # lookup_field = 'id'

    # def get_object(self):
    #     print(self.kwargs)
    #     return Status.objects.get(id=2)


class StatusDeleteAPIView(DestroyAPIView):
    queryset = Status.objects.all()
    # permission_classes = [IsAuthenticated]
    serializer_class = StatusSerializer


class StatusUpdateAPIView(RetrieveUpdateAPIView):
    # permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
