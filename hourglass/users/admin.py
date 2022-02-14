
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from .models import AuditUserEntry


from .forms import UserChangeForm, UserCreationForm
User = get_user_model()


class AuditEntrySectionAdmin(admin.TabularInline):
    model = AuditUserEntry
    extra = 0
    classes = ['collapse']
    readonly_fields = ['action', 'ip', 'created', ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    readonly_fields = ['last_login', 'date_joined', 'login_count']
    fieldsets = auth_admin.UserAdmin.fieldsets + (


        (
            "Personal Info", {"fields": ("note", "phone",)}
        ),
    )
    list_display = ["username", "is_staff", "is_active", "date_joined", "last_login", "email", 'login_count']
    search_fields = ["username", "email", "id", ]
    ordering = ('-date_joined',)
    inlines = [AuditEntrySectionAdmin]

    def login_count(self, obj):
        return obj.login_count


