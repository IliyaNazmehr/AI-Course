from django.contrib import admin
from .models import SummaryHistory


@admin.register(SummaryHistory)
class SummaryHistoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for SummaryHistory model.
    
    Features:
    - Shows user and creation date in the list view.
    - Enables date hierarchy navigation.
    - Displays '-empty-' when a field has no value.
    """
    # Columns shown in the Django admin list
    list_display = ('user', 'created_at')

    # Adds date-based drill-down navigation on top of the list
    date_hierarchy = 'created_at'

    # Display this text if a field is empty (good for readability)
    empty_value_display = "-empty-"

    # Optional improvement: enable filtering in admin sidebar
    list_filter = ('user', 'created_at')

    # Optional improvement: make list searchable
    search_fields = ('user__username', 'input_text', 'summary_text')