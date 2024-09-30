# Savannah-Informatics-Technical-Challenge
### Project Overview

This project implements a simple customer and order management system with the following features:

-   **Authentication and Authorization** using **Auth0**.
-   **CRUD operations** to add, view, and manage customers and orders.
-   **SMS notifications** sent via **Africa's Talking** when an order is created.
-   **Unit testing** with **coverage checking** using Django's test framework and `coverage.py`.
-   **Continuous Integration** with **GitHub Actions**.
-   **Continuous Deployment** to **Heroku**.
`DEBUG has been set to True for access to the browsable API`

### Prerequisites

-   **Python 3.9.6 (64bit)**
-   **Django**
-   **Django Rest Framework**
-   An **Auth0 account** (for authentication and authorization).
-   An **Africa's Talking account** (for SMS functionality).
-   **GitHub** (for CI/CD with GitHub Actions).
-   **Heroku CLI** (for deploying the app).

* * * * *

### Setting up the Project

#### 1\. **Clone the Repository**

`git clone https://github.com/JoelOdhiambo/Savannah-Informatics-Technical-Challenge.git
cd customer_order_api`

#### 2\. **Install Dependencies**

`pip3 install -r requirements.txt`

#### 3\. **Set Up Environment Variables**

You need to create a `.env` file or set environment variables for:

-   **Auth0** credentials.
-   **Africa's Talking** credentials.

Create a `.env` file in the project root and add the following:





`# Auth0 Configuration
AUTH0_CLIENT_ID=your_auth0_client_id
AUTH0_CLIENT_SECRET=your_auth0_client_secret
AUTH0_DOMAIN=your_auth0_domain
AUTH0_AUDIENCE=your_auth0_audience

# Africa's Talking Configuration
AFRICASTALKING_USERNAME=sandbox
AFRICASTALKING_API_KEY=your_africas_talking_api_key`

Alternatively, you can set these environment variables directly on your system.

#### 4\. **Run Database Migrations**

`python3 manage.py migrate`

#### 5\. **Run the Development Server**

`python3 manage.py runserver`

Now, you can access the project at `http://localhost:8000/`.

* * * * *

### Setting up Auth0

1.  **Create an Auth0 account** at [Auth0](https://auth0.com).
2.  **Set up an application** in Auth0 as a **Regular Web Application**.
3.  In the application settings, configure the following:
    -   **Allowed Callback URLs**: `http://localhost:8000/auth/complete/auth0/`
    -   **Allowed Logout URLs**: `http://localhost:8000/`
    -   **Allowed Web Origins**: `http://localhost:8000/`
4.  Add the **Auth0 credentials** (client ID, secret, domain) to your environment variables as shown above.
5.  In case you experience an error from Auth0 stating that the **Allowed Callback URLs** are incorrect, Inspect the **Login with Auth0** URL in your browser's Network tab: => Open Developer Tools in your browser ; => Go to the Network tab and click the login button again ; => Find the network request that goes to Auth0 ; => Look at the redirect_uri parameter that is being sent in the request to Auth0. The `redirect_uri` will be something like: `http://localhost:8000/auth/complete/auth0?redirect_state=FBWxxoJ5P02TxnlAo11gLn6bYZLoiiqS`. Use that as the Callback URL.


* * * * *

### Running Tests and Checking Coverage

You can run the unit tests and check coverage using `coverage.py`:

1.  **Run Unit Tests**:

    `coverage run --source='.' python3 manage.py test`

2.  **Generate Coverage Report**:  

    `coverage report`

3.  **Generate an HTML Coverage Report** (optional):

    `coverage html`

The **HTML coverage report** will be generated in the `htmlcov/` directory, and you can open it in your browser to view detailed coverage.

* * * * *

### Continuous Integration (CI) with GitHub Actions

We use **GitHub Actions** to automatically run tests and check coverage every time code is pushed to the repository.

#### CI Workflow Setup

The GitHub Actions workflow is already set up in the repository under `.github/workflows/django.yml`. It automatically:

-   Sets up a Python environment.
-   Installs dependencies.
-   Runs database migrations.
-   Executes tests and generates a coverage report.

You can view the status of the CI jobs on your repository's **Actions** tab on GitHub.

* * * * *

### Continuous Deployment (CD) to Heroku

The app is deployed to **Heroku**. Every time code is pushed to the **main branch**, Heroku automatically redeploys the app.

#### Setting up Heroku

1.  **Install the Heroku CLI**:

    `curl https://cli-assets.heroku.com/install.sh | sh`

2.  **Create a Heroku App**:

    `heroku create your-app-name`

3.  **Configure Environment Variables on Heroku**:

    `heroku config:set AUTH0_CLIENT_ID=your_auth0_client_id
    heroku config:set AUTH0_CLIENT_SECRET=your_auth0_client_secret
    heroku config:set AUTH0_DOMAIN=your_auth0_domain
    heroku config:set AFRICASTALKING_API_KEY=your_africas_talking_api_key`

4.  **Deploy to Heroku**:

    `git push heroku main`

5.  **Enable Automatic Deployments** on Heroku by linking your GitHub repository to Heroku:

    -   Go to the **Heroku Dashboard**.
    -   Select your app and navigate to the **Deploy** tab.
    -   Connect to your GitHub repository and enable automatic deployments for the **main** branch.

* * * * *

