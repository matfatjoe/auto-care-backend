from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from authentication.models import Profile

from services.models import Service
from services.serializers import ServiceSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    """Handles CRUD operations for Services."""

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(user=profile)

    def perform_update(self, serializer):
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(user=profile)

    def get_queryset(self):
        return Service.objects.filter(is_deleted=False, user=self.request.user.profile)

    def destroy(self, request, *args, **kwargs):
        service = self.get_object()
        service.is_deleted = True
        service.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
