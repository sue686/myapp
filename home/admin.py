from django.contrib import admin
from django.contrib.auth.models import Permission
# Register your models here.
from .models import UserProfile,Department,EmailGroup,EmailAddress


class EmailAddressAdmin(admin.ModelAdmin):
    list_display = ('email','groupname')

admin.site.register(Permission)
admin.site.register(UserProfile)
admin.site.register(Department)
admin.site.register(EmailGroup)
admin.site.register(EmailAddress,EmailAddressAdmin)
