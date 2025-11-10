from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, WishlistItem, Transaction, SavingPlan, Reminder, Destination

class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Custom Profile', {
            'fields': ('nick_name', 'phone_number', 'gender', 'language'),
        }),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Custom Profile', {
            'fields': ('nick_name', 'phone_number', 'gender', 'language'),
        }),
    )

admin.site.register(User, UserAdmin)
admin.site.register(WishlistItem)
admin.site.register(Transaction)
admin.site.register(SavingPlan)
admin.site.register(Reminder)
admin.site.register(Destination)