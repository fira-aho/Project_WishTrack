from django.contrib import admin
from .models import User, WishlistItem, Transaction, SavingPlan

admin.site.register(User)
admin.site.register(WishlistItem)
admin.site.register(Transaction)
admin.site.register(SavingPlan)