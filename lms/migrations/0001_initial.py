# Generated by Django 5.0.6 on 2025-03-22 08:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_number', models.CharField(help_text="Customer's unique identifier.", max_length=20, unique=True)),
                ('first_name', models.CharField(blank=True, help_text="Customer's first name.", max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, help_text="Customer's last name.", max_length=100, null=True)),
                ('date_of_birth', models.DateField(blank=True, help_text="Customer's date of birth.", null=True)),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
            },
        ),
        migrations.CreateModel(
            name='LoanRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_number', models.CharField(help_text="Customer's unique identifier.", max_length=20, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, help_text='Amount requested for the loan.', max_digits=12)),
                ('status', models.CharField(default='Pending', help_text='Current status of the loan request (e.g., Pending, Approved, Rejected).', max_length=20)),
                ('token', models.CharField(blank=True, help_text='Token received from the Scoring Engine for querying the score.', max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp when the loan request was created.')),
                ('approved_limit', models.DecimalField(blank=True, decimal_places=2, help_text='Approved loan limit after scoring.', max_digits=12, null=True)),
                ('score', models.IntegerField(blank=True, help_text='Score received from the Scoring Engine.', null=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_number', models.CharField(help_text="Customer's unique identifier.", max_length=20, unique=True)),
                ('subscription_date', models.DateTimeField(auto_now_add=True, help_text='Timestamp when the customer subscribed.')),
                ('status', models.CharField(default='Active', help_text='Current status of the subscription (e.g., Active, Inactive).', max_length=20)),
            ],
            options={
                'ordering': ['-subscription_date'],
            },
        ),
        migrations.CreateModel(
            name='ScoringResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(help_text='Score received from the Scoring Engine.')),
                ('limit_amount', models.DecimalField(decimal_places=2, help_text='Recommended loan limit from the Scoring Engine.', max_digits=12)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp when the scoring result was recorded.')),
                ('loan_request', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='scoring_result', to='lms.loanrequest')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
