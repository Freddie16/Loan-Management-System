from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch
from .models import LoanRequest, Customer
import json
from django.conf import settings

class LoanTests(TestCase):
    """
    Test suite for the loan management APIs.
    This class contains test methods to verify the functionality of the loan management module.
    """

    def setUp(self):
        """
        Set up test data and client for each test method.
        This method is called before each test to ensure a clean state.
        """
        self.client = APIClient()
        self.customer_number = "test_customer_123"
        self.loan_amount = 1000.00
        self.loan_request_data = {
            "customer_number": self.customer_number,
            "amount": self.loan_amount
        }

    def test_loan_request_api(self):
        """
        Test the loan request API endpoint.
        This test verifies that a loan request can be successfully created.
        """
        url = reverse('loan-request')  # Assuming you've named your URL 'loan-request'
        response = self.client.post(url, data=self.loan_request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Or appropriate status
        self.assertEqual(LoanRequest.objects.count(), 1)
        self.assertEqual(LoanRequest.objects.first().customer_number, self.customer_number)

    def test_loan_status_api(self):
        """
        Test the loan status API endpoint.
        This test verifies that the loan status can be retrieved for a given customer.
        """
        # First, create a loan request
        LoanRequest.objects.create(customer_number=self.customer_number, amount=self.loan_amount, status="Approved")
        url = reverse('loan-status', kwargs={'customer_number': self.customer_number})  # Assuming URL name 'loan-status'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['status'], "Approved")

    def test_loan_request_duplicate(self):
        """
        Test handling of duplicate loan requests.
        This test verifies that a customer cannot apply for another loan if there's an ongoing request.
        """
        LoanRequest.objects.create(customer_number=self.customer_number, amount=self.loan_amount, status="Pending")
        url = reverse('loan-request')
        response = self.client.post(url, data=self.loan_request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # Or appropriate error status

    @patch('lms.views.requests.get')  # Mock the scoring engine API call
    def test_loan_request_scoring_engine_success(self, mock_get):
        """
        Test loan request with successful scoring engine response.
        This test verifies the loan request flow when the scoring engine returns a success response.
        """
        # Mock the scoring engine response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = lambda: {"score": 700, "limitAmount": 5000}

        url = reverse('loan-request')
        response = self.client.post(url, data=self.loan_request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Or appropriate success status
        loan_request = LoanRequest.objects.first()
        self.assertEqual(loan_request.status, "Approved")  # Or your success status

    @patch('lms.views.requests.get')
    def test_loan_request_scoring_engine_failure(self, mock_get):
        """
        Test loan request with scoring engine failure.
        This test verifies the loan request flow when the scoring engine returns an error.
        """
        # Mock the scoring engine response
        mock_get.return_value.status_code = 500
        mock_get.return_value.json = lambda: {"error": "Scoring failed"}

        url = reverse('loan-request')
        response = self.client.post(url, data=self.loan_request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)  # Or appropriate error status
        loan_request = LoanRequest.objects.first()
        self.assertEqual(loan_request.status, "Rejected")  # Or your failure status

    @patch('lms.views.requests.get')
    def test_loan_request_scoring_engine_retry_success(self, mock_get):
        """
        Test loan request with scoring engine retry success.
        This test verifies the retry mechanism when the scoring engine initially fails but eventually succeeds.
        """
        # Mock the scoring engine response to fail a few times then succeed
        responses = [
            MockResponse(500, json.dumps({"error": "Scoring temporarily unavailable"})),
            MockResponse(500, json.dumps({"error": "Scoring temporarily unavailable"})),
            MockResponse(200, json.dumps({"score": 700, "limitAmount": 5000})),
        ]
        mock_get.side_effect = responses

        url = reverse('loan-request')
        response = self.client.post(url, data=self.loan_request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Or appropriate success status
        loan_request = LoanRequest.objects.first()
        self.assertEqual(loan_request.status, "Approved")  # Or your success status

    @patch('lms.views.requests.get')
    def test_loan_request_scoring_engine_retry_failure(self, mock_get):
        """
        Test loan request with scoring engine retry failure.
        This test verifies the retry mechanism when the scoring engine consistently fails.
        """
        # Mock the scoring engine response to fail repeatedly
        responses = [
            MockResponse(500, json.dumps({"error": "Scoring temporarily unavailable"}))] * (settings.RETRY_COUNT + 1)
        mock_get.side_effect = responses

        url = reverse('loan-request')
        response = self.client.post(url, data=self.loan_request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)  # Or appropriate error status
        loan_request = LoanRequest.objects.first()
        self.assertEqual(loan_request.status, "Failed")  # Or your failure status

    # Add tests for transaction data API
    # Add tests for KYC API integration (mocking external calls)
    # Add tests for edge cases like invalid input, missing data, etc.

class MockResponse:
    """
    Helper class to mock requests.Response objects.
    """
    def __init__(self, status_code, content):
        self.status_code = status_code
        self.content = content

    def json(self):
        return json.loads(self.content)