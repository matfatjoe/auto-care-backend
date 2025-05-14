from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from clients.models import Client
from clients.serializers import ClientSerializer
from authentication.models import Profile


class ClientViewSet(viewsets.ModelViewSet):
    """Handles CRUD operations for Clients."""

    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(user=profile)

    def get_queryset(self):
        return Client.objects.filter(is_deleted=False, user=self.request.user.profile)

    def perform_update(self, serializer):
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(user=profile)

    def destroy(self, request, *args, **kwargs):
        client = self.get_object()
        client.is_deleted = True
        client.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
