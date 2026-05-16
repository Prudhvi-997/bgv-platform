"""
Unit tests for the TenantManager + tenant_context primitives.

We exercise the manager against a throwaway model installed in the
accounts app's `tests_app_label` namespace at test-collection time.
"""
import uuid

from django.core.exceptions import PermissionDenied
from django.db import connection, models
from django.test import TransactionTestCase

from apps.accounts.managers import TenantManager
from apps.accounts.tenant_context import (
    get_current_tenant,
    set_current_tenant,
    reset_current_tenant,
    tenant_scope,
    unfiltered_scope,
)


class TenantThing(models.Model):
    """In-test model — exercises TenantManager without pulling other apps."""

    tenant_id = models.UUIDField()
    label = models.CharField(max_length=32)

    objects = TenantManager()

    class Meta:
        app_label = "accounts"


class TenantContextTests(TransactionTestCase):
    """
    Uses TransactionTestCase instead of TestCase so that the schema_editor
    can create our throwaway model outside an outer atomic() block —
    SQLite cannot toggle FK checks mid-transaction.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with connection.schema_editor() as editor:
            editor.create_model(TenantThing)

    @classmethod
    def tearDownClass(cls):
        with connection.schema_editor() as editor:
            editor.delete_model(TenantThing)
        super().tearDownClass()

    def setUp(self):
        self.tenant_a = uuid.uuid4()
        self.tenant_b = uuid.uuid4()
        with unfiltered_scope():
            TenantThing.objects.create(tenant_id=self.tenant_a, label="a-1")
            TenantThing.objects.create(tenant_id=self.tenant_a, label="a-2")
            TenantThing.objects.create(tenant_id=self.tenant_b, label="b-1")

    def test_no_tenant_set_raises_permission_denied(self):
        # Make absolutely sure no tenant is set in this context.
        token = set_current_tenant(None)
        try:
            with self.assertRaises(PermissionDenied):
                list(TenantThing.objects.all())
        finally:
            reset_current_tenant(token)

    def test_tenant_scope_filters_to_one_tenant(self):
        with tenant_scope(self.tenant_a):
            self.assertEqual(TenantThing.objects.count(), 2)
            self.assertTrue(
                all(t.tenant_id == self.tenant_a for t in TenantThing.objects.all())
            )
        with tenant_scope(self.tenant_b):
            self.assertEqual(TenantThing.objects.count(), 1)

    def test_unfiltered_scope_returns_everything(self):
        with unfiltered_scope():
            self.assertEqual(TenantThing.objects.count(), 3)

    def test_unfiltered_method_escapes(self):
        # Even without an unfiltered_scope, the explicit .unfiltered() method
        # on the manager should bypass tenant filtering.
        token = set_current_tenant(None)
        try:
            self.assertEqual(TenantThing.objects.unfiltered().count(), 3)
        finally:
            reset_current_tenant(token)

    def test_contextvar_get_and_set(self):
        original = get_current_tenant()
        token = set_current_tenant(self.tenant_a)
        try:
            self.assertEqual(get_current_tenant(), self.tenant_a)
        finally:
            reset_current_tenant(token)
        self.assertEqual(get_current_tenant(), original)
