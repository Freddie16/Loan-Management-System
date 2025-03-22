from django.urls import path
from . import views

urlpatterns = [
    path('request/', views.loan_request, name='loan-request'),
    path('status/<str:customer_number>/', views.loan_status, name='loan-status'),
    path('transactions/', views.transaction_data, name='transaction-data'),
    path('subscribe/', views.subscribe, name='subscribe'),  # Add URL for Subscription API
    path('scoring/initiate/<str:customer_number>/', views.initiate_scoring_query, name='initiate-scoring'),
    path('scoring/result/<str:token>/', views.get_scoring_result, name='get-scoring-result'),
]