"""
Root URL configuration.

Each portal has its own BFF mounted under a distinct prefix. The BFFs
are the primary security boundary (CLAUDE.md Part 4.3, Layer 1) — a
candidate session token can only reach `/api/candidate/`, never
`/api/ops/`, regardless of RBAC permissions.
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # Authentication endpoints are pre-portal — the client does not yet
    # have a portal scope until the JWT is issued. Subsequent requests
    # flow to /api/<portal>/ and hit Layer-1 enforcement at the BFF.
    path("api/auth/", include("apps.accounts.urls")),
    path("api/ops/", include("bff.ops_bff.urls")),
    path("api/client/", include("bff.client_bff.urls")),
    path("api/candidate/", include("bff.candidate_bff.urls")),
    path("api/vendor/", include("bff.vendor_bff.urls")),
    path("api/admin/", include("bff.admin_bff.urls")),
]
