from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, History


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'card_id')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'card_id', 'first_name', 'last_name', 'is_staff')


class HistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'key', 'time_cr', 'user_id', 'active', 'time_back')


admin.site.register(CustomUser, MyUserAdmin)
admin.site.register(History, HistoryAdmin)
