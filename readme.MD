# Django Channels Chat Application

This is a real-time chat application built with Django, Django Rest Framework (DRF), and Django Channels. It uses JSON Web Tokens (JWT) for authentication and WebSockets for live, bidirectional communication between the server and clients.

## Features

*   **User Authentication**: Secure user registration and login using JWT (Access and Refresh tokens).
*   **Real-time Chat**: Instant messaging between users via WebSockets.
*   **Chat History**: Messages are persisted in the database.
*   **Scalable Backend**: Utilizes Django Channels and a Redis channel layer for handling concurrent WebSocket connections.
*   **Custom User Model**: A flexible user model for easy extension.

## Technologies Used

*   **Backend**:
    *   Python 3.x
    *   Django
    *   Django Rest Framework (DRF)
    *   Django Channels
    *   `djangorestframework-simplejwt` for JWT Authentication
    *   `channels_redis` for the channel layer
*   **Database**: SQLite3 (for development)
*   **Cache/Broker**: Redis

## Prerequisites

Before you begin, ensure you have the following installed on your system:

*   Python (3.8 or newer)
*   Pip (Python package installer)
*   Redis Server

## Installation and Setup

Follow these steps to get your development environment set up.

1.  **Clone the Repository**

    ```bash
    git clone <your-repository-url>
    cd channellearn
    ```

2.  **Create and Activate a Virtual Environment**

    *   On macOS and Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Install Dependencies**

    Create a `requirements.txt` file with the necessary packages:

    ```
    Django
    djangorestframework
    channels
    channels_redis
    djangorestframework-simplejwt
    PyJWT
    ```

    Then, install them using pip:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Start Redis**

    Make sure your Redis server is running on its default port (6379). You can start it with:

    ```bash
    redis-server
    ```

5.  **Apply Database Migrations**

    This will create the database schema for the `accounts` and `notifications` apps.

    ```bash
    python manage.py migrate
    ```

6.  **Create a Superuser**

    This allows you to access the Django admin panel.

    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the Development Server**

    The application uses ASGI, so you'll run it with Django's `runserver` command, which supports it automatically.

    ```bash
    python manage.py runserver
    ```

    The application will be available at `http://127.0.0.1:8000`.
