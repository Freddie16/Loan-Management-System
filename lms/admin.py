from django.contrib import admin
from .models import LoanRequest, Customer  # Import your models
from .models import Subscription  # Import Subscription model

# Register your models here.

@admin.register(LoanRequest)
class LoanRequestAdmin(admin.ModelAdmin):
    """
    Admin configuration for the LoanRequest model.
    This allows LoanRequest objects to be managed through the Django admin interface.
    """
    list_display = ('customer_number', 'amount', 'status', 'token')
    list_filter = ('status',)
    search_fields = ('customer_number',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Customer model.
    This allows Customer objects to be managed through the Django admin interface.
    """
    list_display = ('customer_number',)
    search_fields = ('customer_number',)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Subscription model.
    This allows Subscription objects to be managed through the Django admin interface.
    """
    list_display = ('customer_number', 'subscription_date', 'status')  # Customize as needed
    list_filter = ('status',)
    search_fields = ('customer_number',)