"""
Database router enforcing the CLAUDE.md Part 4.8 isolation rule:

    All analytics, dashboard, BI, and report queries MUST read from the
    Reporting DB. Direct queries to the operational database for any
    reporting or analytics purpose are a build-breaking architectural
    defect.

The `apps.reporting` bounded context is bound to the `reporting`
connection. Every other app uses `default` (operational). Cross-database
relations and cross-database migrations are explicitly denied.
"""


class ReportingRouter:
    """Route the `reporting` app exclusively to the `reporting` DB."""

    REPORTING_APP_LABEL = "reporting"
    REPORTING_DB_ALIAS = "reporting"
    OPERATIONAL_DB_ALIAS = "default"

    def db_for_read(self, model, **hints):
        if model._meta.app_label == self.REPORTING_APP_LABEL:
            return self.REPORTING_DB_ALIAS
        return self.OPERATIONAL_DB_ALIAS

    def db_for_write(self, model, **hints):
        # The reporting DB is read-only at the application level
        # (CLAUDE.md Part 4.8.4). Only the sync mechanism (log shipping
        # in Phase 1, CDC in Phase 2/3) writes to it. Application-layer
        # writes to a reporting-app model still target the reporting DB
        # — but only the migrate command should ever do that.
        if model._meta.app_label == self.REPORTING_APP_LABEL:
            return self.REPORTING_DB_ALIAS
        return self.OPERATIONAL_DB_ALIAS

    def allow_relation(self, obj1, obj2, **hints):
        # Disallow cross-DB FK/relations entirely. A reporting read
        # model never joins to an operational table via ORM.
        same_app = obj1._meta.app_label == obj2._meta.app_label
        if same_app:
            return True
        if (
            obj1._meta.app_label == self.REPORTING_APP_LABEL
            or obj2._meta.app_label == self.REPORTING_APP_LABEL
        ):
            return False
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == self.REPORTING_APP_LABEL:
            return db == self.REPORTING_DB_ALIAS
        return db == self.OPERATIONAL_DB_ALIAS
