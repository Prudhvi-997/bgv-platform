"""Django admin registration for the accounts app (minimal)."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import OTPCode, Role, User, UserRole


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    ordering = ("-created_at",)
    list_display = ("email", "full_name", "portal", "tenant_id", "is_active", "is_staff")
    list_filter = ("portal", "is_active", "is_staff")
    search_fields = ("email", "full_name")
    readonly_fields = ("id", "created_at", "updated_at", "last_login")
    fieldsets = (
        (None, {"fields": ("id", "email", "password")}),
        ("Profile", {"fields": ("full_name", "portal", "tenant_id")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Timestamps", {"fields": ("last_login", "created_at", "updated_at")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "full_name", "portal", "password1", "password2"),
        }),
    )


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "portal", "created_at")
    list_filter = ("portal",)
    search_fields = ("name",)


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "tenant_id", "assigned_at")
    list_filter = ("role",)
    search_fields = ("user__email", "role__name")
    readonly_fields = ("assigned_at",)


@admin.register(OTPCode)
class OTPCodeAdmin(admin.ModelAdmin):
    """Read-only listing — OTPs are sensitive; we never edit them via admin."""

    list_display = ("user", "is_used", "expires_at", "created_at")
    list_filter = ("is_used",)
    search_fields = ("user__email",)
    readonly_fields = ("id", "user", "code", "expires_at", "is_used", "created_at")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
