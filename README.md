#       Loan Management System (LMS)

##       Overview

This project implements a Loan Management System (LMS) as part of a technical assessment. The LMS facilitates loan processing by integrating with a Scoring Engine and a CORE Banking System. It provides RESTful APIs for communication with a mobile application and interacts with SOAP APIs for KYC and transaction data. [cite: 6, 7, 8, 9, 10, 11, 12, 13, 14]

##       Features

*             Subscription API: Allows mobile applications to submit customer numbers. [cite: 17, 18]
*             Loan Request API: Handles loan requests from mobile applications, including customer number and loan amount. [cite: 18, 19]
*             Loan Status API: Enables mobile applications to query the status of a loan. [cite: 19, 20]
*             Transaction Data API: Exposes customer transaction data to the Scoring Engine. [cite: 28, 29, 30, 31, 32, 33, 34]
*             Integration with KYC API: Fetches customer information from the CORE Banking System using SOAP. [cite: 15, 16, 35]
*             Integration with Transaction Data API: Retrieves historical transactional records from the CORE Banking System using SOAP. [cite: 15, 16, 35]
*             Scoring Engine Integration:
    *                   Initiates scoring queries. [cite: 23, 24, 35, 36, 37]
    *                   Retrieves scoring results with a retry mechanism. [cite: 24, 25, 26, 27, 36, 37]
*             Loan application failure mechanism if scoring engine doesn't respond after retries. [cite: 26, 27]

##       Architecture

The system architecture involves the following components:

*             Mobile Application: Interacts with the LMS via RESTful APIs. [cite: 17, 18, 19, 20, 21]
*             LMS Module:
    *                   Exposes RESTful APIs. [cite: 17, 18, 19, 20, 21]
    *                   Integrates with the Scoring Engine (REST). [cite: 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34]
    *                   Consumes data from the CORE Banking System (SOAP). [cite: 15, 16]
*             Scoring Engine: Provides customer scores and loan limits. [cite: 6, 7, 8, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34]
*             CORE Banking System: Provides KYC and transaction data. [cite: 6, 15, 16, 35]

##       API Endpoints

###               KYC API

*                   WSDL URL: [https://kycapitest.credable.io/service/customerWsdl.wsdl](https://kycapitest.credable.io/service/customerWsdl.wsdl) [cite: 35]

###               Transaction Data API

*                   WSDL URL: [https://trxapitest.credable.io/service/transactionWsdl.wsdl](https://trxapitest.credable.io/service/transactionWsdl.wsdl) [cite: 35]

###               Scoring APIs

*                   **Step 1: Initiate Query Score**
    *                         URL: [https://scoringtest.credable.io/api/v1/scoring/initiateQueryScore/{customerNumber}](https://scoringtest.credable.io/api/v1/scoring/initiateQueryScore/{customerNumber}) [cite: 35, 36, 37]
    *                         Method: GET
    *                         Header: `client-token`
    *                         Response:

        ```json
        {
          "token": "generated_token"
        }
        ```
*                   **Step 2: Query the score**
    *                         URL: [https://scoringtest.credable.io/api/v1/scoring/queryScore/{token}](https://scoringtest.credable.io/api/v1/scoring/queryScore/{token}) [cite: 35, 36, 37]
    *                         Method: GET
    *                         Header: `client-token`
    *                         Response:

        ```json
        {
          "id": 9,
          "customerNumber": "",
          "score": 564,
          "limitAmount": 30000,
          "exclusion": "No Exclusion",
          "exclusionReason": "No Exclusion"
        }
        ```

###               Create Client API

*                   URL: [https://scoringtest.credable.io/api/v1/client/createClient](https://scoringtest.credable.io/api/v1/client/createClient) [cite: 32, 33, 34]
*                   Method: POST
*                   Request Payload:

        ```json
        {
          "url": "[YOUR ENDPOINT URL]",
          "name": "[NAME OF YOUR SERVICE]",
          "username": "[BASIC AUTHENTICATION USERNAME]",
          "password": "[BASIC AUTHENTICATION PASSWORD]"
        }
        ```
*                   Response:

        ```json
        {
          "id": 0, // generated client id
          "url": "[YOUR ENDPOINT]",
          "name": "[NAME OF YOUR SERVICE]",
          "username": "[BASIC AUTHENTICATION USERNAME]",
          "password": "[BASIC AUTHENTICATION PASSWORD]",
          "token": "[GENERATED UNIQUE UUID]" // use this to make call
          for scoring
        }
        ```

###               Transaction Data Response Format

```json
[
  {
    "accountNumber": "332216783322167555621628",
    "alternativechanneltrnscrAmount": 87988.2441,
    "alternativechanneltrnscrNumber": 0,
    "alternativechanneltrnsdebitAmount": 675.3423,
    "alternativechanneltrnsdebitNumber": 902403930,
    "atmTransactionsNumber": 4812921,
    "atmtransactionsAmount": 561.96661249,
    "bouncedChequesDebitNumber": 8,
    "bouncedchequescreditNumber": 0,
    "bouncedchequetransactionscrAmount": 748011.19,
    "bouncedchequetransactionsdrAmount": 43345.569028578,
    "chequeDebitTransactionsAmount": 4.6933076819151E8,
    "chequeDebitTransactionsNumber": 44,
    "createdAt": 740243532000,
    "createdDate": 1196266216000,
    "credittransactionsAmount": 609.297663,
    "debitcardpostransactionsAmount": 21.134264,
    "debitcardpostransactionsNumber": 502,
    "fincominglocaltransactioncrAmount": 0.0,
    "id": 2,
    "incominginternationaltrncrAmount": 70.52733936,
    "incominginternationaltrncrNumber": 9,
    "incominglocaltransactioncrNumber": 876,
    "intrestAmount": 310118,
    "lastTransactionDate": 1169339429000,
    "lastTransactionType": null,
    "lastTransactionValue": 3,
    "maxAtmTransactions": 6.0,
    "maxMonthlyBebitTransactions": 5.66201073E8,
    "maxalternativechanneltrnscr": 0.0,
    "maxalternativechanneltrnsdebit": 0.0,
    "maxbouncedchequetransactionscr": 0.0,
    "maxchequedebittransactions": 0.0,
    "maxdebitcardpostransactions": 5.18696078798654E15,
    "maxincominginternationaltrncr": 0.0,
    "maxincominglocaltransactioncr": 0.0,
    "maxmobilemoneycredittrn": 0.0,
    "maxmobilemoneydebittransaction": 0.0,
    "maxmonthlycredittransactions": 0.0,
    "maxoutgoinginttrndebit": 0.0,
    "maxoutgoinglocaltrndebit": 0.0,
    "maxoverthecounterwithdrawals": 959858.0,
    "minAtmTransactions": 0.0,
    "minMonthlyDebitTransactions": 0.0,
    "minalternativechanneltrnscr": 0.0,
    "minalternativechanneltrnsdebit": 0.0,
    "minbouncedchequetransactionscr": 0.0,
    "minchequedebittransactions": 0.0,
    "mindebitcardpostransactions": 4.539102239610779E15,
    "minincominginternationaltrncr": 0.0,
    "minincominglocaltransactioncr": 0.0,
    "minmobilemoneycredittrn": 0.0,
    "minmobilemoneydebittransaction": 524.0,
    "minmonthlycredittransactions": 0.0,
    "minoutgoinginttrndebit": 0.0,
    "minoutgoinglocaltrndebit": 0.0,
    "minoverthecounterwithdrawals": 5821338.0,
    "mobilemoneycredittransactionAmount": 0.0,
    "mobilemoneycredittransactionNumber": 946843,
    "mobilemoneydebittransactionAmount": 0.0,
    "mobilemoneydebittransactionNumber": 5523407,
    "monthlyBalance": 6.59722841E8,
    "monthlydebittransactionsAmount": 103262.90429936,
    "outgoinginttransactiondebitAmount": 5.473303560725E7,
    "outgoinginttrndebitNumber": 646,
    "outgoinglocaltransactiondebitAmount": 565972.1236,
    "outgoinglocaltransactiondebitNumber": 2971,
    "overdraftLimit": 0.0,
    "overthecounterwithdrawalsAmount": 332.0,
    "overthecounterwithdrawalsNumber": 87569,
    "transactionValue": 1.0,
    "updatedAt": 773556430000
  },
  {
    "accountNumber": "332216783322167555621628",
    "alternativechanneltrnscrAmount": 27665.6889301,
    "alternativechanneltrnscrNumber": 0,
    "alternativechanneltrnsdebitAmount": 2.9997265951905E7,
    "alternativechanneltrnsdebitNumber": 114,
    "atmTransactionsNumber": 36934417,
    "atmtransactionsAmount": 192538.94,
    "bouncedChequesDebitNumber": 535,
    "bouncedchequescreditNumber": 0,
    "bouncedchequetransactionscrAmount": 1.37,
    "bouncedchequetransactionsdrAmount": 2602.4,
    "chequeDebitTransactionsAmount": 2765.57,
    "chequeDebitTransactionsNumber": 6,
    "createdAt": 1401263420000,
    "createdDate": 1350538588000,
    "credittransactionsAmount": 0.0,
    "debitcardpostransactionsAmount": 117347.063,
    "debitcardpostransactionsNumber": 931309756,
    "fincominglocaltransactioncrAmount": 2552389.4,
    "id": 5,
    "incominginternationaltrncrAmount": 76.160425,
    "incominginternationaltrncrNumber": 285700400,
    "incominglocaltransactioncrNumber": 1,
    "intrestAmount": 22,
    "lastTransactionDate": 554704439000,
    "lastTransactionType": null,
    "lastTransactionValue": 1,
    "maxAtmTransactions": 0.0,
    "maxMonthlyBebitTransactions": 7.8272009E7,
    "maxalternativechanneltrnscr": 0.0,
    "maxalternativechanneltrnsdebit": 0.0,
    "maxbouncedchequetransactionscr": 0.0,
    "maxchequedebittransactions": 0.0,
    "maxdebitcardpostransactions": 5.468080253826023E15,
    "maxincominginternationaltrncr": 0.0,
    "maxincominglocaltransactioncr": 0.0,
    "maxmobilemoneycredittrn": 0.0,
    "maxmobilemoneydebittransaction": 0.0,
    "maxmonthlycredittransactions": 0.0,
    "maxoutgoinginttrndebit": 0.0,
    "maxoutgoinglocaltrndebit": 0.0,
    "maxoverthecounterwithdrawals": 6.09866462E8,
    "minAtmTransactions": 0.0,
    "minMonthlyDebitTransactions": 0.0,
    "minalternativechanneltrnscr": 0.0,
    "minalternativechanneltrnsdebit": 0.0,
    "minbouncedchequetransactionscr": 0.0,
    "minchequedebittransactions": 0.0,
    "mindebitcardpostransactions": 4.716295906413E12,
    "minincominginternationaltrncr": 0.0,
    "minincominglocaltransactioncr": 0.0,
    "minmobilemoneycredittrn": 0.0,
    "minmobilemoneydebittransaction": 0.0,
    "minmonthlycredittransactions": 29624.78,
    "minoutgoinginttrndebit": 0.0,
    "minoutgoinglocaltrndebit": 0.0,
    "minoverthecounterwithdrawals": 1.00927826E8,
    "mobilemoneycredittransactionAmount": 349693.8071922,
    "mobilemoneycredittransactionNumber": 4092,
    "mobilemoneydebittransactionAmount": 1.87382823746E7,
    "mobilemoneydebittransactionNumber": 0,
    "monthlyBalance": 2205.0,
    "monthlydebittransactionsAmount": 295.6677,
    "outgoinginttransactiondebitAmount": 9.561730814,
    "outgoinginttrndebitNumber": 0,
    "outgoinglocaltransactiondebitAmount": 56.03,
    "outgoinglocaltransactiondebitNumber": 0,
    "overdraftLimit": 7.0,
    "overthecounterwithdrawalsAmount": 3.72849038239E8,
    "overthecounterwithdrawalsNumber": 546382904,
    "transactionValue": 51.0,
    "updatedAt": 687774305000
  }
]
Setup and Installation
Clone the repository:

Bash

git clone <repository_url>
cd loan_management_system
Create a virtual environment (recommended):

Bash

python3 -m venv venv
source venv/bin/activate # On Linux/macOS
# venv\Scripts\activate # On Windows
Install dependencies:

Bash

pip install -r requirements.txt
Database setup:

Development:

Bash

python manage.py migrate
The application is configured to use SQLite for development. Running python manage.py migrate will set up the database. No additional configuration is needed unless you intend to use a different database system.
Environment variables:

Set the necessary environment variables.
SECRET_KEY: A secret key for your Django project.
Run the development server:

Bash

python manage.py runserver
Deployment
The application is designed for deployment on platforms like Render.

Render Deployment
Create a Render account and project.

Connect your repository to Render.

Configure the web service:

Environment: Python 3

Build Command:

Bash

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
Start Command:

Bash

gunicorn your_project_name.wsgi --bind 0.0.0.0:$PORT
Environment Variables:

SECRET_KEY: Your Django secret key.
Ensure ALLOWED_HOSTS in settings.py is correctly configured for your Render domain.

After deployment, use the Render-provided URL for your Transaction Data API in the createClient API call.

Testing
API Testing
Use tools like Postman or curl to test the API endpoints.

Create Client: Test the createClient API to register your Transaction Data API.
Loan Requests: Test the Loan Request API.
Loan Status: Verify the Loan Status API.
Scoring Engine Integration: Test the complete loan request flow to ensure correct interaction with the Scoring Engine, including retries.
Test Data
Use the following Customer IDs for testing:

234774784
318411216
340397370
366585630
397178638
Project Structure
LOAN/
├── loan_management_system/  (Project settings)
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── lms/                     (Our application)
│   ├── migrations/
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│   ├───serializers.py
├── manage.py
├───requirements.txt
├───Procfile
