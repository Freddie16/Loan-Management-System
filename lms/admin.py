from django.contrib import admin
from .models import LoanRequest, Customer, Subscription, ScoringResult

# Register your models here.
@admin.register(LoanRequest)
class LoanRequestAdmin(admin.ModelAdmin):
    list_display = ('customer_number', 'amount', 'status', 'created_at', 'approved_limit', 'score')
    list_filter = ('status', 'created_at')
    search_fields = ('customer_number', 'status')
    readonly_fields = ('created_at',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_number', 'first_name', 'last_name', 'date_of_birth')
    search_fields = ('customer_number', 'first_name', 'last_name')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('customer_number', 'subscription_date', 'status')
    list_filter = ('status', 'subscription_date')
    search_fields = ('customer_number',)

@admin.register(ScoringResult)
class ScoringResultAdmin(admin.ModelAdmin):
    list_display = ('loan_request', 'score', 'limit_amount', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('loan_request__customer_number',)