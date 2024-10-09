# Stark Challenge

## Overview

When running the docker-compose, it is possible to follow the execution inside the bash.  
In the scheduler, invoices are created through the `create_invoices` function, which is called by `setup_scheduler`, 
where it is configured to trigger the `create_invoices` function every 3 hours.  
To simulate the webhook, I used ngrok to expose the endpoint from local machine.  
Thus, every time the webhook receives a notification, I get the request in my app/webhook and log the event.

## Project Structure

The project is organized into the following main components:

- **`app.py`**: The entry point for the Flask application.
- **`webhook_handler.py`**: Contains the logic to handle incoming webhook requests.
- **`services/`**: Contains application logic, including invoicing and scheduling services.
  - **`invoicer.py`**: Handles invoice creation and related operations.
  - **`scheduler.py`**: Sets up and manages scheduled tasks using APScheduler.
- **`tests/`**: Contains unit tests for the application components.
  - **`test_scheduler.py`**
  - **`test_webhook_handler.py`**
  - **`test_invoicer.py`**
- **`.env`**: Environment variables configuration file.
- **`requirements.txt`**: Lists the Python dependencies for the project.
- **`Dockerfile`**: Configuration file for building the Docker image.
- **`docker-compose.yml`**: Docker Compose configuration for setting up the development environment with Ngrok.
- **`README.md`**: Documentation for the project.

## Setup and Installation

### Prerequisites

- Docker
- Docker Compose

### Building and Running the Application

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd <repository-folder>

2. **Build the Docker Image**:
    
    ```bash
    docker-compose build
3. **Start the Application**:
    ```bash
    docker-compose up


## API Endpoints
### Authentication
Basic authentication is used to secure the endpoints. Use the following credentials for authentication:

- **Username:** vs_tech_challenge
- **Password:** SuperSecurePassword123@

### Endpoints
**1. Webhook**
- **Description:** ```Receives webhook events from StarkBank and processes them accordingly.```
- **Endpoint:** ```POST /webhook```
- **Request Body:**
    ```json
  {
  "subscription": "invoice",
  "log": {
    "type": "invoice.paid",
    "invoice": {
      "id": "inv_123",
      "amount": 200,
      "due": "2024-11-01T00:00:00Z"
    }
  }
}

- **Response:**
    ```json
    {
        "message": "Webhook Received Successfully"
    }
  
## Testing and Coverage

### Preparing the environment 💻
How is nothing too complex the environment is more prepared for perform tests

Execute:
(os & Linux)

#### 1 - `virtualenv .venv` 
#### 2 - `source .venv/bin/activate` 

(Windows)

#### 1 - `python -m venv .venv` 
#### 2 - `source .venv/Scripts/activate` 

#### 3 - `pip install -r requirements.txt` 


To run the tests, use the following command:
  ```bash
    pytest
  ```

### Generating Coverage Report

To generate a coverage report, follow these steps:

1. **Be on the environment that you created .venv:**


2. **Run Coverage Analysis:**

    ```bash
    coverage run -m pytest /tests
    ```

3. **Generate the Coverage Report:**

    ```bash
    coverage report
    ```

4. **Generate an HTML Coverage Report:**

    ```bash
    coverage html
    ```

    The HTML report can be viewed by opening `htmlcov/index.html` in a web browser.

**Coverage Status:** The project achieves 98% test coverage. 🎇
