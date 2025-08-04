**Subscription Management System**
Welcome to the Subscription Management System, a Django-based web application for managing subscription plans, user subscriptions, and fetching USD to BDT exchange rates periodically using Celery.
This README provides clear instructions to set up, run, and test the project, including its features and troubleshooting notes.

**Table of Contents**
1. Features
2. Prerequisites
4. Configuration
5. Testing the API with Postman
6. Verifying Celery Tasks
7. Troubleshooting
9. Notes on Celery and Redis Installation

**1. Features**
The Subscription Management System includes the following features:
  **i. Django Admin Interface:**
        Manage subscription plans, user subscriptions, and exchange rate logs.
        Accessible at http://127.0.0.1:8000/admin/.
        Username: admin
        Password: 1234
  **ii. Frontend UI:**
      A Bootstrap-based table displaying user subscriptions.
      Accessible at http://127.0.0.1:8000/subscriptions/.
      There is a Subscription list table with columns : Username, Plan, Start Date, End Date, Status
      
  **iii. REST API:**
      Secure endpoints for managing subscriptions, protected by JWT authentication.
      Endpoints: 
          1. /api/token/ (for authentication) and /api/token/refresh/ (for refresh token when it will get expired)
          2. /api/subscribe/ (for new subscription)
          2. /api/subscriptions/ (for subscription data).
          4. /api/cancel/ ( to cancel a subscription)
          5. /api/exchange-rate/?base=USD&target=BDT (for exchange rate data)
          6. /subscriptions/-----> frontend UI to see the subscription list
          
    **iv. Periodic Exchange Rate Updates:**
    A Celery task (fetch_usd_to_bdt_exchange_rate) fetches USD to BDT exchange rates hourly using the ExchangeRate-API.
    Results are stored in the ExchangeRateLog model and viewable in the Django Admin. Here I tried. I will discuss below.



**2. Prerequisites**
Before setting up the project, ensure must have:

amqp==5.3.1 , asgiref==3.9.1 , billiard==4.2.1 , celery==5.3.4 , certifi==2025.7.14, charset-normalizer==3.4.2, click==8.2.1, click-didyoumean==0.3.1
click-plugins==1.1.1.2, click-repl==0.3.0 , colorama==0.4.6, cron-descriptor==1.4.5, Django==4.2.23, django-celery-beat==2.5.0, django-celery-results==2.5.1, django-filter==25.1 
django-timezone-field==7.1, djangorestframework==3.16.0, djangorestframework-simplejwt==5.3.0, idna==3.10, kombu==5.5.4, Markdown==3.8.2
mysqlclient @ file:///E:/Projects%20Django/Django%20REST/Subscription%20Management/mysqlclient-2.2.7-cp312-cp312-win_amd64.whl#sha256=4b4c0200890837fc64014cc938ef2273252ab544c1b12a6c1d674c23943f3f2e
packaging==25.0, prompt_toolkit==3.0.51, PyJWT==2.10.1, python-crontab==3.3.0, python-dateutil==2.9.0,.post0 python-decouple==3.8, redis==5.0.1, requests==2.31.0, setuptools==80.9.0, six==1.17.0
sqlparse==0.5.3, tzdata==2025.2, urllib3==2.5.0, vine==5.1.0, wcwidth==0.2.13


**Create and Activate a Virtual Environment:**
      python -m venv subscription_env
      subscription_env\Scripts\activate


**Install Dependencies:**
These all are listed in Requirements.txt
Create a requirements.txt file with:django==4.2.7
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
mysqlclient==2.2.0
celery==5.3.4
redis==5.0.1
requests==2.31.0
python-decouple==3.8
django-celery-beat==2.5.0
django-celery-results==2.5.1
setuptools==70.0.0
**Install:pip install -r requirements.txt**


**Install Redis:**
Download and install Memurai or Redis for Windows.
Start Redis:redis-server.exe
Verify:redis-cli ping
Should return PONG.


**Install MariaDB (via XAMPP):**
Start XAMPP Control Panel and enable MariaDB (must need 10.5 or more upgraded version).

**Configuration**
Create a .env File:

In the project root (E:\Projects Django\Django REST\Subscription Management), create a .env file
DEBUG=True
DB_NAME=subscription_db
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=django-db
EXCHANGE_RATE_API_KEY=9cb72f07672bb6791c76f40a



EXCHANGE_RATE_API_KEY: Verify it works:curl https://v6.exchangerate-api.com/v6/9cb72f07672bb6791c76f40a/latest/USD
If invalid, get a new key from ExchangeRate-API.


**Apply Database Migrations:**
python manage.py migrate


**Create a Superuser for Django Admin:**
python manage.py createsuperuser


**Running the Project**

1. Start Redis:
    redis-server.exe
   
3. Start the Django Server:
    python manage.py runserver


4. Access at http://127.0.0.1:8000.


 i. Start the Celery Worker:
    In a new terminal:
    subscription_env\Scripts\activate
    celery -A subscription_system worker --loglevel=info

  ii. Start Celery Beat (for scheduled tasks):
    In another terminal:subscription_env\Scripts\activate
    celery -A subscription_system beat --loglevel=info

  **iii. Testing the API with Postman**
    The REST API uses JWT authentication. Use Postman to test some endpoints, Here I describe below:

            1. Get a JWT Token: Use a Username and Password to get a token
              Request: POST to http://127.0.0.1:8000/api/token/
              ex. Body: x-www-form-urlencodedusername="samim"
             ex.  password=s@123456


              Create a Test User (to get a access token):from django admin panel
                sername='samim'
                password='s@123456
              
              Response: JSON with access and refresh tokens.
              From here copy the access token and need for make a particular user subscription.
              Check in Postman.

              2. POST a New Subscription
              http://127.0.0.1:8000/api/subscribe/
              Here just need the previous access token to complete a subscription and if the token showing invalid
              then check for http://127.0.0.1:8000/api/token/refresh/ to get a refresh token.

              http://127.0.0.1:8000/api/subscriptions to check the data of the subscriptions.
              
              4. If it needed to cancel a subscription 
              http://127.0.0.1:8000/api/cancel/ ,it will require subscription_id ,check the id from database and 
              hit the api to cancel a subscription.Then status will be changed to cancel.

              5. To check the current exchnage rate USD to BDT / you can modify the api for BDT to USD,,,
              hit 
              http://127.0.0.1:8000/api/exchange-rate/?base=USD&target=BDT
              It will add new exchange rate log in database.


              6. Access Subscriptions:

              Request: GET to http://127.0.0.1:8000/api/subscriptions/
              Headers:Authorization: Bearer <access_token>
              Get response like below:
                        [
                {
                    "id": 2,
                    "user": 3,
                    "plan": 2,
                    "start_date": "2025-08-02T18:11:55Z",
                    "end_date": "2025-08-31T18:12:04Z",
                    "status": "active"
                },
                {
                    "id": 3,
                    "user": 3,
                    "plan": 3,
                    "start_date": "2025-08-03T23:50:29.898680Z",
                    "end_date": "2025-11-01T23:50:29.898680Z",
                    "status": "active"
                },
                {
                    "id": 4,
                    "user": 3,
                    "plan": 1,
                    "start_date": "2025-08-04T00:14:16.686279Z",
                    "end_date": "2025-09-03T00:14:16.686279Z",
                    "status": "cancelled"
                },
            ]



**Verifying Celery Tasks**
The project uses Celery to fetch USD to BDT exchange rates hourly, storing results in ExchangeRateLog. 



**Troubleshooting**
I have faced some difficulties as for first time in celery and Redis
Redis Connection Error:
Ensure Redis is running (redis-cli ping returns PONG).
Verify CELERY_BROKER_URL=redis://localhost:6379/0 in .env.

Task Not Running:
Check worker logs for errors.

Notes on Celery and Redis Installation
As a new user to Celery and Redis, I attempted to implement these components for periodic task scheduling.
However, I suspect they may not be working correctly due to initial configuration issues (e.g., incorrect Redis URLs like redis://redis:6379/0). 
The current setup uses redis://localhost:6379/0 and django-celery-results for task results. If you encounter issues:

Verify Redis: Ensure redis-server.exe is running and accessible.
Check Celery Logs: Look for errors in worker or Beat logs.
Reinstall Dependencies
The tasks will be added in TASK RESULT in Django DB.

Contact for Support

