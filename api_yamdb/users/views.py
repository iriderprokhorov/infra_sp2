import uuid

from django.core.mail import send_mail
from rest_framework import viewsets, filters, status, permissions
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .permissions import IsAdminOrSuper
from .serializers import (
    CustomUserSerializer,
    SignUpSerializer,
    TokenSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAdminOrSuper,)
    lookup_field = "username"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)

    @action(
        detail=False,
        methods=["get", "patch"],
        url_path="me",
        url_name="me",
        serializer_class=CustomUserSerializer,
        permission_classes=(permissions.IsAuthenticated,),
    )
    def me(self, request):
        me_user = request.user
        serializer = self.get_serializer(me_user)
        if request.method == "PATCH":
            serializer = self.get_serializer(
                me_user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(email=me_user.email, role=me_user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignUpView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            username = serializer.validated_data.get("username")
            confirmation_code = uuid.uuid4()
            User.objects.create(
                username=username,
                email=email,
                confirmation_code=confirmation_code,
                is_active=False,
            )
            send_mail(
                "Ваш код подтверждения",
                f"Ваш код: {confirmation_code}",
                "test@example.com",
                [email],
                fail_silently=False,
            )

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class TokenView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get("username")
        confirmation_code = serializer.validated_data.get(
            "confirmation_code")
        user = get_object_or_404(User, username=username)
        if confirmation_code == user.confirmation_code:
            user.is_active = True
            user.save()
            access_token = AccessToken.for_user(user)
            return Response(
                {"token": str(access_token)}, status=status.HTTP_200_OK
            )

        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
