from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import SENTINELLE, COUNTRY, CustomUser,Laboratoire

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'country')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'country')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Country info', {'fields': ('country',)}),
    )

admin.site.register(SENTINELLE)
admin.site.register(Laboratoire)
admin.site.register(COUNTRY)



# Register your models here.
