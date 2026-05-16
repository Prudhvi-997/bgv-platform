"""
Operations Portal BFF — aggregates domain service calls for the
ops UI. Domain logic lives in `apps.cases`, `apps.verification`,
`apps.compliance`, etc. The BFF only orchestrates and projects.
"""
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsOpsPortalSession


class HealthView(APIView):
    """Liveness probe for the Ops BFF."""

    permission_classes = [IsOpsPortalSession]

    def get(self, request):
        return Response({"portal": "ops", "status": "ok"})
