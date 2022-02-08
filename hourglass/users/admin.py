
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from .models import AuditEntry


from .forms import UserChangeForm, UserCreationForm
User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    readonly_fields = ['last_login', 'date_joined']
    fieldsets = auth_admin.UserAdmin.fieldsets + (


        (
            "Personal Info", {"fields": ("note", "phone",)}
        ),
    )
    list_display = ["username", "is_staff", "is_active", "date_joined", "last_login", "email"]
    search_fields = ["username", "email", "id", ]
    ordering = ('-date_joined',)


@admin.register(AuditEntry)
class AuditEntryAdmin(admin.ModelAdmin):
    list_display = ['action', 'username', 'ip',]
    list_filter = ['action',]
