
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model


from .forms import UserChangeForm, UserCreationForm
User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    readonly_fields = ['last_login']
    fieldsets = auth_admin.UserAdmin.fieldsets + (
        (
            "User", {"fields": ("note", "phone", "photo")}
        ),
    )
    list_display = ["username", "is_superuser", "is_active", "date_joined", "last_login", "email"]
    search_fields = ["username", "email", "id", ]
    ordering = ('-date_joined',)
