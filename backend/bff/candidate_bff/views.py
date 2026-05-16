"""
Candidate Portal BFF — aggregates domain service calls for the portal UI.
Domain logic lives in the `apps.*` packages. The BFF only orchestrates.
"""
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsCandidatePortalSession


class HealthView(APIView):
    """Liveness probe for the Candidate Portal BFF."""

    permission_classes = [IsCandidatePortalSession]

    def get(self, request):
        return Response({"portal": "candidate", "status": "ok"})
