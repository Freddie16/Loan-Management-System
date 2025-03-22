from rest_framework import serializers
from .models import LoanRequest  # Import your LoanRequest model


class LoanRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for handling loan requests.
    """
    class Meta:
        model = LoanRequest
        fields = ['customer_number', 'amount']  # Specify the fields to include
        #if you want all fields, you can use fields = '__all__'


class LoanResponseSerializer(serializers.Serializer):
    """
    Serializer for loan responses.
    """
    loan_id = serializers.IntegerField(allow_null=True, read_only=True)
    status = serializers.CharField(max_length=20, read_only=True)
    message = serializers.CharField(max_length=255, read_only=True)


class LoanStatusResponseSerializer(serializers.Serializer):
    """
    Serializer for loan status responses.
    """
    customer_number = serializers.CharField(max_length=20)
    status = serializers.CharField(max_length=20)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, allow_null=True)
    # Add other fields as needed


class TransactionDataSerializer(serializers.Serializer):
    """
    Serializer for transaction data.
    
    This serializer defines the structure for the transaction data
    exchanged with the Scoring Engine.  Ensure field types and
    validation match the Scoring Engine's API documentation.
    """
    accountNumber = serializers.CharField(max_length=255)  # Example, adjust max_length
    alternativechanneltrnscrAmount = serializers.FloatField()
    alternativechanneltrnscrNumber = serializers.IntegerField()
    alternativechanneltrnsdebitAmount = serializers.FloatField()
    alternativechanneltrnsdebitNumber = serializers.IntegerField()
    atmTransactionsNumber = serializers.IntegerField()
    atmtransactionsAmount = serializers.FloatField()
    bouncedChequesDebitNumber = serializers.IntegerField()
    bouncedchequescreditNumber = serializers.IntegerField()
    bouncedchequetransactionscrAmount = serializers.FloatField()
    bouncedchequetransactionsdrAmount = serializers.FloatField()
    chequeDebitTransactionsAmount = serializers.FloatField()
    chequeDebitTransactionsNumber = serializers.IntegerField()
    createdAt = serializers.IntegerField()
    createdDate = serializers.IntegerField()
    credittransactionsAmount = serializers.FloatField()
    debitcardpostransactionsAmount = serializers.FloatField()
    debitcardpostransactionsNumber = serializers.IntegerField()
    fincominglocaltransactioncrAmount = serializers.FloatField()
    id = serializers.IntegerField()
    incominginternationaltrncrAmount = serializers.FloatField()
    incominginternationaltrncrNumber = serializers.IntegerField()
    incominglocaltransactioncrNumber = serializers.IntegerField()
    intrestAmount = serializers.IntegerField()
    lastTransactionDate = serializers.IntegerField()
    lastTransactionType = serializers.CharField(allow_null=True, max_length=255)  # Example
    lastTransactionValue = serializers.IntegerField()
    maxAtmTransactions = serializers.FloatField()
    maxMonthlyBebitTransactions = serializers.FloatField()
    maxalternativechanneltrnscr = serializers.FloatField()
    maxalternativechanneltrnsdebit = serializers.FloatField()
    maxbouncedchequetransactionscr = serializers.FloatField()
    maxchequedebittransactions = serializers.FloatField()
    maxdebitcardpostransactions = serializers.FloatField()
    maxincominginternationaltrncr = serializers.FloatField()
    maxincominglocaltransactioncr = serializers.FloatField()
    maxmobilemoneycredittrn = serializers.FloatField()
    maxmobilemoneydebittransaction = serializers.FloatField()
    maxmonthlycredittransactions = serializers.FloatField()
    maxoutgoinginttrndebit = serializers.FloatField()
    maxoutgoinglocaltrndebit = serializers.FloatField()
    maxoverthecounterwithdrawals = serializers.FloatField()
    minAtmTransactions = serializers.FloatField()
    minMonthlyDebitTransactions = serializers.FloatField()
    minalternativechanneltrnscr = serializers.FloatField()
    minalternativechanneltrnsdebit = serializers.FloatField()
    minbouncedchequetransactionscr = serializers.FloatField()
    minchequedebittransactions = serializers.FloatField()
    mindebitcardpostransactions = serializers.FloatField()
    minincominginternationaltrncr = serializers.FloatField()
    minincominglocaltransactioncr = serializers.FloatField()
    minmobilemoneycredittrn = serializers.FloatField()
    minmobilemoneydebittransaction = serializers.FloatField()
    minmonthlycredittransactions = serializers.FloatField()
    minoutgoinginttrndebit = serializers.FloatField()
    minoutgoinglocaltrndebit = serializers.FloatField()
    minoverthecounterwithdrawals = serializers.FloatField()
    mobilemoneycredittransactionAmount = serializers.FloatField()
    mobilemoneycredittransactionNumber = serializers.IntegerField()
    mobilemoneydebittransactionAmount = serializers.FloatField()
    mobilemoneydebittransactionNumber = serializers.IntegerField()
    monthlyBalance = serializers.FloatField()
    monthlydebittransactionsAmount = serializers.FloatField()
    outgoinginttransactiondebitAmount = serializers.FloatField()
    outgoinginttrndebitNumber = serializers.IntegerField()
    outgoinglocaltransactiondebitAmount = serializers.FloatField()
    outgoinglocaltransactiondebitNumber = serializers.IntegerField()
    overdraftLimit = serializers.FloatField()
    overthecounterwithdrawalsAmount = serializers.FloatField()
    overthecounterwithdrawalsNumber = serializers.IntegerField()
    transactionValue = serializers.FloatField()
    updatedAt = serializers.IntegerField()