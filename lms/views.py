import requests
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny
from .serializers import LoanRequestSerializer, LoanResponseSerializer, LoanStatusResponseSerializer
from .models import LoanRequest, Customer, Subscription, ScoringResult  # Import new models
from zeep import Client
import time
from django.conf import settings
from django.shortcuts import get_object_or_404
import json  # Import the json module
import logging


# Settings for external APIs (replace with actual values - ideally from environment variables)
SCORING_ENGINE_BASE_URL = settings.SCORING_ENGINE_BASE_URL
SCORING_ENGINE_CLIENT_URL = settings.SCORING_ENGINE_CLIENT_URL
KYC_WSDL_URL = settings.KYC_WSDL_URL
TRANSACTION_WSDL_URL = settings.TRANSACTION_WSDL_URL
CORE_BANKING_USERNAME = settings.CORE_BANKING_USERNAME
CORE_BANKING_PASSWORD = settings.CORE_BANKING_PASSWORD

# Settings for retry mechanism
RETRY_COUNT = settings.RETRY_COUNT
RETRY_DELAY = settings.RETRY_DELAY  # seconds

# Client token (replace with the token obtained from client creation)
# CLIENT_TOKEN = "your_client_token"
CLIENT_TOKEN = None  # Initialize as None, fetch it when needed


# Function to register the client with the scoring engine
def register_client():
    global CLIENT_TOKEN
    if CLIENT_TOKEN:
        return CLIENT_TOKEN

    url = SCORING_ENGINE_CLIENT_URL
    payload = {
        "url": settings.SCORING_ENGINE_ENDPOINT_URL,
        "name": "LMS Service",
        "username": settings.CORE_BANKING_USERNAME,
        "password": settings.CORE_BANKING_PASSWORD
    }
    
    try:
        # Log the request for debugging
        logger.info(f"Register client request: URL={url}, Payload={payload}")
        
        response = requests.post(url, json=payload)
        
        # Log the response for debugging
        logger.info(f"Register client response: Status={response.status_code}, Content={response.text}")
        
        response.raise_for_status()
        response_data = response.json()
        CLIENT_TOKEN = response_data.get("token")
        logger.info(f"Client token received: {CLIENT_TOKEN}")
        return CLIENT_TOKEN
    except requests.exceptions.RequestException as e:
        logger.error(f"Error registering client: {e}")
        logger.error(f"Response content: {response.content if 'response' in locals() else 'No response'}")
        return None



# Function to fetch customer KYC data
logger = logging.getLogger(__name__)

def get_customer_kyc(customer_number):
    """
    Fetches customer information from the KYC API using the provided customer number.
    """
    try:
        logger.info(f"Fetching KYC data for customer: {customer_number}")
        client = Client(KYC_WSDL_URL)
        logger.info(f"KYC WSDL URL: {KYC_WSDL_URL}")
        
        # Construct the request
        request_data = {"customerNumber": customer_number}
        
        # Make the SOAP request
        response = client.service.getKYC(**request_data)
        logger.info(f"KYC API response: {response}")
        
        return response
    except Exception as e:
        logger.error(f"Error fetching KYC data for customer {customer_number}: {e}", exc_info=True)
        return None

# Function to fetch transaction data
def get_transaction_data(customer_number):
    """
    Fetches transaction data from the CORE Banking System API for a given customer.
    Transforms the data into the format expected by the Scoring Engine.
    """
    try:
        client = Client(TRANSACTION_WSDL_URL)
        response = client.service.getTransactions(customer_number)
        transaction_data = []
        for item in response:
            transaction_data.append({
                "accountNumber": item.accountNumber,
                "alternativechanneltrnscrAmount": item.alternativechanneltrnscrAmount,
                "alternativechanneltrnscrNumber": item.alternativechanneltrnscrNumber,
                "alternativechanneltrnsdebitAmount": item.alternativechanneltrnsdebitAmount,
                "alternativechanneltrnsdebitNumber": item.alternativechanneltrnsdebitNumber,
                "atmTransactionsNumber": item.atmTransactionsNumber,
                "atmtransactionsAmount": item.atmtransactionsAmount,
                "bouncedChequesDebitNumber": item.bouncedChequesDebitNumber,
                "bouncedchequescreditNumber": item.bouncedchequescreditNumber,
                "bouncedchequetransactionscrAmount": item.bouncedchequetransactionscrAmount,
                "bouncedchequetransactionsdrAmount": item.bouncedchequetransactionsdrAmount,
                "chequeDebitTransactionsAmount": item.chequeDebitTransactionsAmount,
                "chequeDebitTransactionsNumber": item.chequeDebitTransactionsNumber,
                "createdAt": item.createdAt,
                "createdDate": item.createdDate,
                "credittransactionsAmount": item.credittransactionsAmount,
                "debitcardpostransactionsAmount": item.debitcardpostransactionsAmount,
                "debitcardpostransactionsNumber": item.debitcardpostransactionsNumber,
                "fincominglocaltransactioncrAmount": item.fincominglocaltransactioncrAmount,
                "fincominglocaltransactioncrNumber": item.incominglocaltransactioncrNumber,
                "incominginternationaltrncrAmount": item.incominginternationaltrncrAmount,
                "incominginternationaltrncrNumber": item.incominginternationaltrncrNumber,
                "intrestAmount": item.intrestAmount,
                "lastTransactionDate": item.lastTransactionDate,
                "lastTransactionType": item.lastTransactionType,
                "lastTransactionValue": item.lastTransactionValue,
                "maxAtmTransactions": item.maxAtmTransactions,
                "maxMonthlyBebitTransactions": item.maxMonthlyBebitTransactions,
                "maxalternativechanneltrnscr": item.maxalternativechanneltrnscr,
                "maxalternativechanneltrnsdebit": item.maxalternativechanneltrnsdebit,
                "maxbouncedchequetransactionscr": item.maxbouncedchequetransactionscr,
                "maxchequedebittransactions": item.maxchequedebittransactions,
                "maxdebitcardpostransactions": item.maxdebitcardpostransactions,
                "maxincominginternationaltrncr": item.maxincominginternationaltrncr,
                "maxincominglocaltransactioncr": item.maxincominglocaltransactioncr,
                "maxmobilemoneycredittrn": item.maxmobilemoneycredittrn,
                "maxmobilemoneydebittransaction": item.maxmobilemoneydebittransaction,
                "maxmonthlycredittransactions": item.maxmonthlycredittransactions,
                "maxoutgoinginttrndebit": item.maxoutgoinginttrndebit,
                "maxoutgoinglocaltrndebit": item.maxoutgoinglocaltrndebit,
                "maxoverthecounterwithdrawals": item.maxoverthecounterwithdrawals,
                "minAtmTransactions": item.minAtmTransactions,
                "minMonthlyDebitTransactions": item.minMonthlyDebitTransactions,
                "minalternativechanneltrnscr": item.minalternativechanneltrnscr,
                "minalternativechanneltrnsdebit": item.minalternativechanneltrnsdebit,
                "minbouncedchequetransactionscr": item.minbouncedchequetransactionscr,
                "minchequedebittransactions": item.minchequedebittransactions,
                "mindebitcardpostransactions": item.mindebitcardpostransactions,
                "minincominginternationaltrncr": item.minincominginternationaltrncr,
                "minincominglocaltransactioncr": item.minincominglocaltransactioncr,
                "minmobilemoneycredittrn": item.minmobilemoneycredittrn,
                "minmobilemoneydebittransaction": item.minmobilemoneydebittransaction,
                "minmonthlycredittransactions": item.minmonthlycredittransactions,
                "minoutgoinginttrndebit": item.minoutgoinglocaltrndebit,
                "minoverthecounterwithdrawals": item.minoverthecounterwithdrawals,
                "mobilemoneycredittransactionAmount": item.mobilemoneycredittransactionAmount,
                "mobilemoneycredittransactionNumber": item.mobilemoneycredittransactionNumber,
                "mobilemoneydebittransactionAmount": item.mobilemoneydebittransactionAmount,
                "mobilemoneydebittransactionNumber": item.mobilemoneydebittransactionNumber,
                "monthlyBalance": item.monthlyBalance,
                "monthlydebitTransactionsAmount": item.monthlydebitTransactionsAmount,
                "monthlydebittransactionsNumber": item.monthlydebittransactionsNumber,
                "onusChequesTransactionsAmount": item.onusChequesTransactionsAmount,
                "onusChequesTransactionsNumber": item.onusChequesTransactionsNumber,
                "outgoinginternationaltrndrAmount": item.outgoinginternationaltrndrAmount,
                "outgoinginternationaltrndrNumber": item.outgoinginternationaltrndrNumber,
                "outgoinglocaltrndrAmount": item.outgoinglocaltrndrAmount,
                "outgoinglocaltrndrNumber": item.outgoinglocaltrndrNumber,
                "overTheCounterCreditTransactionsAmount": item.overTheCounterCreditTransactionsAmount,
                "overTheCounterCreditTransactionsNumber": item.overthecounterwithdrawalsAmount,
                "posTransactionsAmount": item.posTransactionsNumber,
                "salaryAmount": item.salaryAmount,
                "salaryDate": item.salaryDate,
                "totalBouncedCheques": item.totalBouncedCheques,
                "totalChequeTransactions": item.totalChequeTransactions,
                "totalCreditTransactions": item.totalCreditTransactions,
                "totalDebitTransactions": item.totalDebitTransactions,
                "totalIncomingTransactions": item.totalIncomingTransactions,
                "totalMobileMoneyTransactions": item.totalMobileMoneyTransactions,
                "totalOutgoingTransactions": item.totalOutgoingTransactions,
                "totalTransactions": item.totalTransactions,
                "transactionDate": item.transactionDate,
                "transactionTime": item.transactionTime,
                "transactionType": item.transactionType,
                "transactionValue": item.transactionValue
            })
        return transaction_data
    except Exception as e:
        logger.error(f"Error fetching transaction data for customer {customer_number}: {e}", exc_info=True)
        return None


# Function to initiate scoring query and handle retries
def initiate_scoring_query(customer_number, amount):
    """
    Initiates a scoring query with the Scoring Engine and handles retries.
    """
    global CLIENT_TOKEN
    if not CLIENT_TOKEN:
        CLIENT_TOKEN = register_client()
        if not CLIENT_TOKEN:
            return None, "Error registering client with Scoring Engine"

    # This URL format should match the documentation
    url = f"{SCORING_ENGINE_BASE_URL}/initiateQueryScore"
    
    # The payload should include customerNumber, amount, and clientToken
    payload = {
        "customerNumber": customer_number,
        "amount": float(amount),  # Ensure amount is sent as a number
        "clientToken": CLIENT_TOKEN
    }
    
    headers = {
        'Content-Type': 'application/json',
        'client-token': CLIENT_TOKEN  # Add this header as per documentation
    }

    for attempt in range(RETRY_COUNT + 1):
        try:
            response = requests.post(url, json=payload, headers=headers)
            
            # Log the request and response for debugging
            logger.info(f"Scoring Engine request: URL={url}, Payload={payload}, Headers={headers}")
            logger.info(f"Scoring Engine response: Status={response.status_code}, Content={response.text}")
            
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.json(), None
        except requests.exceptions.RequestException as e:
            logger.error(f"Attempt {attempt + 1} failed: {e}")
            logger.error(f"Response content: {response.content if 'response' in locals() else 'No response'}")
            
            if attempt == RETRY_COUNT:
                return None, f"Scoring Engine request failed after {RETRY_COUNT} retries"
            time.sleep(RETRY_DELAY)  # Wait before retrying


# Function to get the scoring result
def get_scoring_result(token):
    """
    Retrieves the scoring result from the Scoring Engine using the provided token.
    """
    url = f"{SCORING_ENGINE_BASE_URL}/queryScore/{token}"
    
    # Add the client token in the header as specified in the documentation
    headers = {'client-token': CLIENT_TOKEN}
    
    try:
        response = requests.get(url, headers=headers)
        
        # Log the request and response for debugging
        logger.info(f"Get scoring result request: URL={url}, Headers={headers}")
        logger.info(f"Get scoring result response: Status={response.status_code}, Content={response.text}")
        
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting scoring result: {e}")
        logger.error(f"Response content: {response.content if 'response' in locals() else 'No response'}")
        return None, "Error retrieving scoring result"

@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def loan_request(request):
    logger.info("Received loan request: %s", request.data)
    
    serializer = LoanRequestSerializer(data=request.data)
    if not serializer.is_valid():
        logger.error("Invalid loan request data: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    customer_number = serializer.validated_data['customer_number']
    amount = serializer.validated_data['amount']
    logger.info("Processing loan request for customer: %s, amount: %s", customer_number, amount)

    # Check for existing pending loan request
    if LoanRequest.objects.filter(customer_number=customer_number, status="Pending").exists():
        logger.warning("Loan request already pending for customer: %s", customer_number)
        return Response({"error": "A loan request is already pending for this customer."},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        # Fetch KYC data
        kyc_data = get_customer_kyc(customer_number)
        if not kyc_data:
            logger.error("Failed to retrieve KYC data for customer: %s", customer_number)
            return Response({"error": "Failed to retrieve KYC data."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Store customer data
        customer, created = Customer.objects.update_or_create(
            customer_number=customer_number,
            defaults={
                'first_name': kyc_data.firstName,
                'last_name': kyc_data.lastName,
                'date_of_birth': kyc_data.dateOfBirth,
                # ... other KYC fields
            }
        )

        # Create LoanRequest object first with pending status
        loan_request = serializer.save(
            customer_number=customer_number,
            status="Pending"
        )

        # Initiate scoring query
        scoring_response, scoring_error = initiate_scoring_query(customer_number, amount)
        if scoring_error:
            loan_request.status = "Failed"
            loan_request.save()
            logger.error("Scoring query failed for customer: %s, error: %s", customer_number, scoring_error)
            return Response({"error": scoring_error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        token = scoring_response.get("token")
        if not token:
            loan_request.status = "Failed"
            loan_request.save()
            logger.error("No token received from scoring engine for customer: %s", customer_number)
            return Response({"error": "No token received from scoring engine"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Update the loan request with the token
        loan_request.token = token
        loan_request.save()

        # Get scoring result
        scoring_result, result_error = get_scoring_result(token)
        if result_error:
            loan_request.status = "Failed"
            loan_request.save()
            logger.error("Failed to get scoring result for token: %s, error: %s", token, result_error)
            return Response({"error": result_error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Process scoring result
        score = scoring_result.get("score")
        limit_amount = scoring_result.get("limitAmount")

        if score >= 600:  # Example threshold
            loan_request.status = "Approved"
            loan_request.approved_limit = limit_amount
        else:
            loan_request.status = "Rejected"

        loan_request.score = score
        loan_request.save()

        # Create ScoringResult object
        ScoringResult.objects.create(
            loan_request=loan_request,
            score=score,
            limit_amount=limit_amount
        )

        loan_response_data = {
            "customer_number": customer_number,
            "amount": amount,
            "status": loan_request.status,
            "approved_limit": loan_request.approved_limit
        }
        logger.info("Loan request processed successfully: %s", loan_response_data)
        return Response(loan_response_data, status=status.HTTP_200_OK)
    
    except Exception as e:
        # Catch any unexpected exceptions
        logger.exception("Unexpected error processing loan request for customer %s: %s", customer_number, str(e))
        
        # Update loan request status if it was created
        if 'loan_request' in locals():
            loan_request.status = "Failed"
            loan_request.save()
            
        return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def loan_status(request, customer_number):
    """
    API endpoint to retrieve the status of a loan request for a given customer.
    """
    try:
        loan_request = LoanRequest.objects.get(customer_number=customer_number)
        serializer = LoanStatusResponseSerializer(loan_request)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except LoanRequest.DoesNotExist:
        return Response({"error": "Loan request not found for this customer."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def subscribe(request):
    """
    API endpoint to handle customer subscriptions.
    """
    customer_number = request.data.get('customer_number')
    if not customer_number:
        return Response({"error": "Customer number is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Create or update subscription
    subscription, created = Subscription.objects.update_or_create(
        customer_number=customer_number,
        defaults={'status': 'Active'}  # Or get status from request if needed
    )

    if created:
        return Response({"message": f"Subscription created for customer {customer_number}"},
                        status=status.HTTP_201_CREATED)
    else:
        return Response({"message": f"Subscription updated for customer {customer_number}"},
                        status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def transaction_data(request):
    """
    API endpoint to provide transaction data to the Scoring Engine.
    """
    # Assuming the Scoring Engine sends customer_number
    # in the request data. Adjust as needed.
    customer_number = request.data.get('customerNumber')  # Or however the customer number is sent

    if not customer_number:
        return Response({"error": "Customer number is required."}, status=status.HTTP_400_BAD_REQUEST)

    # 1. Fetch transaction data from the CORE Banking System
    transaction_data = get_transaction_data(customer_number)
    if not transaction_data:
        return Response({"error": "Failed to retrieve transaction data."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 2. Return the transaction data in the specified format
    # The get_transaction_data function should already format the data
    # If any transformation is needed, do it here.

    return Response(transaction_data, status=status.HTTP_200_OK)