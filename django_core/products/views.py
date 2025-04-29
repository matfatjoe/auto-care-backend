from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from products.models import Product
from products.serializers import ProductSerializer
from authentication.models import Profile
from rest_framework.response import Response


class ProductViewSet(viewsets.ModelViewSet):
    """Handles CRUD operations for Products."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(user=profile)

    def get_queryset(self):
        return Product.objects.filter(is_deleted=False, user=self.request.user.profile)

    def perform_update(self, serializer):
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(user=profile)

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        product.is_deleted = True
        product.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
