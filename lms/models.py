from django.db import models

class LoanRequest(models.Model):
    """
    Model representing a loan request.
    Stores information about a customer's loan application.
    """
    customer_number = models.CharField(max_length=20, unique=True, help_text="Customer's unique identifier.")
    amount = models.DecimalField(max_digits=12, decimal_places=2, help_text="Amount requested for the loan.")
    status = models.CharField(max_length=20, default="Pending", help_text="Current status of the loan request (e.g., Pending, Approved, Rejected).")
    token = models.CharField(max_length=255, blank=True, null=True, help_text="Token received from the Scoring Engine for querying the score.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the loan request was created.")
    approved_limit = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, help_text="Approved loan limit after scoring.")
    score = models.IntegerField(blank=True, null=True, help_text="Score received from the Scoring Engine.")

    def __str__(self):
        return f"Loan Request for {self.customer_number} - {self.status}"

    class Meta:
        ordering = ['-created_at']  # Order by creation time descending


class Customer(models.Model):
    """
    Model representing customer information.
    Stores relevant details about a customer.
    """
    customer_number = models.CharField(max_length=20, unique=True, help_text="Customer's unique identifier.")
    # Add other customer fields as needed based on KYC API response
    first_name = models.CharField(max_length=100, blank=True, null=True, help_text="Customer's first name.")
    last_name = models.CharField(max_length=100, blank=True, null=True, help_text="Customer's last name.")
    date_of_birth = models.DateField(blank=True, null=True, help_text="Customer's date of birth.")
    # ... other KYC fields

    def __str__(self):
        return f"Customer {self.customer_number}"

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"


class Subscription(models.Model):
    """
    Model representing customer subscriptions.
    Stores information about customer subscriptions to the loan service.
    """
    customer_number = models.CharField(max_length=20, unique=True, help_text="Customer's unique identifier.")
    subscription_date = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the customer subscribed.")
    status = models.CharField(max_length=20, default="Active", help_text="Current status of the subscription (e.g., Active, Inactive).")
    # Add other subscription-related fields as needed

    def __str__(self):
        return f"Subscription for {self.customer_number} - {self.status}"

    class Meta:
        ordering = ['-subscription_date']


class ScoringResult(models.Model):
    """
    Model to store scoring results for loan applications.
    This can be useful for audit trails or further analysis.
    """
    loan_request = models.OneToOneField(LoanRequest, on_delete=models.CASCADE, related_name='scoring_result')
    score = models.IntegerField(help_text="Score received from the Scoring Engine.")
    limit_amount = models.DecimalField(max_digits=12, decimal_places=2, help_text="Recommended loan limit from the Scoring Engine.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the scoring result was recorded.")
    # You might add fields to store the raw response from the Scoring Engine if needed

    def __str__(self):
        return f"Scoring Result for Loan {self.loan_request.customer_number}"

    class Meta:
        ordering = ['-created_at']