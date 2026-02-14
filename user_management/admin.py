from django.contrib import admin
from .models import UserModuleAccess, UserAccessLog, UserAdminNote


@admin.register(UserModuleAccess)
class UserModuleAccessAdmin(admin.ModelAdmin):
    list_display = ['user', 'custom_access_level', 'created_at']
    search_fields = ['user__username', 'user__email']
    list_filter = ['created_at']
    filter_horizontal = ['allowed_categories']
    raw_id_fields = ['user']


@admin.register(UserAccessLog)
class UserAccessLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'ip_address', 'timestamp']
    search_fields = ['user__username', 'action', 'ip_address']
    list_filter = ['timestamp']
    readonly_fields = ['user', 'action', 'ip_address', 'user_agent', 'timestamp']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(UserAdminNote)
class UserAdminNoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'admin', 'is_important', 'created_at']
    search_fields = ['user__username', 'note']
    list_filter = ['is_important', 'created_at']
    raw_id_fields = ['user', 'admin']
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.admin = request.user
        super().save_model(request, obj, form, change)
