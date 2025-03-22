from django.urls import path
from . import views

urlpatterns = [
    # Loan Request API
    path('loans/request/', views.loan_request, name='loan-request'),

    # Loan Status API
    path('loans/status/<str:customer_number>/', views.loan_status, name='loan-status'),

    # Transaction Data API (for Scoring Engine)
    path('loans/transactions/', views.transaction_data, name='transaction-data'),

    # Subscription API
    path('loans/subscribe/', views.subscribe, name='subscribe'),

    # Scoring Engine APIs
    path('scoring/initiate/<str:customer_number>/', views.initiate_scoring_query, name='initiate-scoring'),
    path('scoring/result/<str:token>/', views.get_scoring_result, name='get-scoring-result'),
]