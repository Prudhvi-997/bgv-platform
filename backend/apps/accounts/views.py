"""
Authentication API surface — mounted at `/api/auth/` (see config.urls).

These endpoints are pre-portal: the client does not have a portal scope
until login completes. From the JWT response onward, every request flows
to `/api/<portal>/` and is gated by Layer-1 BFF permission classes
(CLAUDE.md Part 4.3).
"""
from __future__ import annotations

import logging

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import OTPCode
from .serializers import (
    LoginSerializer,
    OTPRequestSerializer,
    OTPVerifySerializer,
    UserSerializer,
)
from .tenant_context import unfiltered_scope
from .tokens import build_tokens_for_user


logger = logging.getLogger(__name__)
User = get_user_model()


# --- Password login (issues JWT with KCheck claims) ------------------------


class LoginView(TokenObtainPairView):
    """POST /api/auth/login/ — email + password → JWT pair."""

    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Auth lookups must hit any user regardless of tenant context.
        with unfiltered_scope():
            return super().post(request, *args, **kwargs)


# --- OTP request / verify (Candidate Portal) -------------------------------


class OTPRequestView(APIView):
    """
    POST /api/auth/otp/request/ — issue an OTP for the given candidate.

    Reply is deliberately uniform whether the user exists or not —
    we do not want this endpoint to act as an email-enumeration oracle.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        with unfiltered_scope():
            user = User.objects.filter(
                email__iexact=email, portal="candidate", is_active=True
            ).first()
            if user:
                otp = OTPCode.generate_for_user(user)
                # TODO(notifications): dispatch via Celery once
                # apps.notifications is implemented. Until then log to
                # stdout so dev / QA can complete the OTP flow.
                logger.info("OTP for %s: %s", user.email, otp.code)

        return Response(
            {"message": "If the account exists, an OTP has been sent."},
            status=status.HTTP_200_OK,
        )


class OTPVerifyView(APIView):
    """POST /api/auth/otp/verify/ — exchange a valid OTP for a JWT pair."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        code = serializer.validated_data["code"]

        with unfiltered_scope():
            user = User.objects.filter(
                email__iexact=email, portal="candidate", is_active=True
            ).first()
            if not user or not OTPCode.verify_for_user(user, code):
                return Response(
                    {"detail": "Invalid or expired OTP."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            tokens = build_tokens_for_user(user)
            payload = UserSerializer(user).data

        return Response(
            {
                "access": tokens["access"],
                "refresh": tokens["refresh"],
                "user": payload,
                "roles": payload["roles"],
            },
            status=status.HTTP_200_OK,
        )


# --- Refresh & logout ------------------------------------------------------


class RefreshView(TokenRefreshView):
    """POST /api/auth/token/refresh/ — rotate refresh, return new access."""

    permission_classes = [AllowAny]


class LogoutView(APIView):
    """POST /api/auth/logout/ — blacklist the supplied refresh token."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh = request.data.get("refresh")
        if not refresh:
            return Response(
                {"detail": "Refresh token required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            token = RefreshToken(refresh)
            token.blacklist()
        except TokenError as exc:
            return Response(
                {"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response({"message": "Logged out."}, status=status.HTTP_200_OK)


# --- Current user ---------------------------------------------------------


class MeView(APIView):
    """GET /api/auth/me/ — return the authenticated user + roles."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        with unfiltered_scope():
            data = UserSerializer(request.user).data
        return Response(data, status=status.HTTP_200_OK)
