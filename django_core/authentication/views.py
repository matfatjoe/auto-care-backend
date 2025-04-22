from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserLoginSerializer
from rest_framework.permissions import IsAuthenticated


class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"]
        )
        if user is not None:
            login(request, user)
            return Response({
                "id": user.id,
                "username": user.username,
                "email": user.email
            }, status=status.HTTP_200_OK)
        return Response(
            {"non_field_errors": ["Invalid credentials."]},
            status=status.HTTP_400_BAD_REQUEST
        )


class LogoutView(APIView):
    """
    View para logout de usuário. Para a autenticação baseada em sessões.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

        # Se o usuário está autenticado, realiza o logout
        request.session.flush()  # Destroi a sessão do usuário
        return Response({"detail": "Logout realizado com sucesso."}, status=status.HTTP_200_OK)
