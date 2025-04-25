# Roll no. 58

# Bookstore Management System (Django & Docker)

![Python Version](https://img.shields.io/badge/python-3.10-blue.svg)
![Django Version](https://img.shields.io/badge/django-4.2-green.svg)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Jenkins](https://img.shields.io/badge/jenkins-%232C5263.svg?style=for-the-badge&logo=jenkins&logoColor=white)

## Project Overview

This project is a full-stack web application for managing an online bookstore, built using Python and the Django framework. It includes features for user authentication, browsing books, adding items to a shopping cart using session storage, and a **custom-built admin panel** for managing book inventory (explicitly avoiding the built-in Django Admin).

The entire application is containerized using Docker and Docker Compose for easy setup, development, and deployment consistency. It also includes a Jenkinsfile to demonstrate a basic CI/CD pipeline for building, testing (optional step included), and deploying the application.

## Features

*   **User Authentication:**
    *   User Registration
    *   User Login / Logout
*   **User Pages:**
    *   View a list of available books.
    *   View detailed information for a single book.
    *   Add books to a persistent shopping cart stored in the user's session.
    *   View and manage the shopping cart (update quantity, remove items).
*   **Custom Admin Panel (Access at `/custom-admin/`):**
    *   Requires staff user login (create via `createsuperuser`).
    *   Add new books to the catalog.
    *   Edit existing book details (title, author, description, price).
    *   Manage book inventory (stock levels).
    *   Delete books from the catalog.
    *   **Note:** This panel is built using Django views and templates, *not* the standard `django.contrib.admin`.
*   **DevOps:**
    *   Fully Dockerized environment using `docker-compose`.
    *   Includes `Dockerfile` for the Django application.
    *   Includes `Jenkinsfile` for CI/CD automation pipeline setup.

## Tech Stack

*   **Backend:** Python 3.10, Django 4.2.x
*   **Database:** MySQL 8.0
*   **Frontend:** HTML5, CSS3, Bootstrap 5 (via CDN)
*   **Server:** Gunicorn (for running Django within Docker)
*   **Containerization:** Docker, Docker Compose
*   **CI/CD:** Jenkins (via `Jenkinsfile`)
*   **DB Driver:** `mysqlclient`
*   **Environment Variables:** `python-dotenv`

## Screenshots & Demo GIF

<!-- Add your screenshots and GIF here! -->
<!-- Suggestions: Homepage (Book List), Book Detail Page, Cart Page, Admin Login, Admin Book List, Admin Add/Edit Form -->

**Homepage (Book List):**
![Screenshot_23-4-2025_18455_127 0 0 1](https://github.com/user-attachments/assets/a8d4732c-49f0-4d89-82e9-7aff1e8f9a4a)

**Book Detail Page:**
![Screenshot_23-4-2025_18550_127 0 0 1](https://github.com/user-attachments/assets/763379cf-5a99-42b6-b057-84b353adf104)

**Shopping Cart:**
![Screenshot_23-4-2025_18550_127 0 0 1](https://github.com/user-attachments/assets/2f8085d2-e3bd-4feb-894b-dedd303f5f92)

**Custom Admin - Book List:**
![Screenshot_23-4-2025_181147_127 0 0 1](https://github.com/user-attachments/assets/a9a4a887-7125-450a-af3d-420a80855c9e)
![image](https://github.com/user-attachments/assets/8fa0b7ea-01d5-47bd-9331-882a9edc2c6c)

**Docker Images:**
![Screenshot 2025-04-23 114631](https://github.com/user-attachments/assets/8ae67cee-11fd-4cca-9adb-1ec3e49df43e)

![image](https://github.com/user-attachments/assets/ff3f4662-4a9d-4a03-ab4a-acefa4d3abcd)

![Screenshot 2025-04-22 231654](https://github.com/user-attachments/assets/1907f60b-a43f-410d-a3a6-930dc093bd82)


**Demo GIF:**

Customer Interface:

![Part1 (1)](https://github.com/user-attachments/assets/2a045ea4-cb43-4ef5-96cb-b46d282a12d6)

Admin Panel:

![Part2](https://github.com/user-attachments/assets/9002a006-0661-4583-b3cc-67ca1ee8900a)



## Prerequisites

Before you begin, ensure you have the following installed on your system:

*   **Git:** For cloning the repository.
*   **Docker:** The containerization platform.
*   **Docker Compose:** For managing multi-container Docker applications (usually included with Docker Desktop).
*   *(Optional)* Python 3.10+ and Pip (if you wish to run outside Docker, though not recommended for this setup).

## Setup & Run Instructions

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Ramharsh-aidev/BookStore
    cd BookStore
    ```

2.  **Configure Environment Variables:**
    *   Create a `.env` file in the project root directory. You can copy the structure from `.env.example` if provided, or create it manually.
    *   **Crucially, set the following variables:**
        *   `SECRET_KEY`: Generate a strong, unique secret key for Django. (You can use online generators or `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`)
        *   `DATABASE_NAME`: e.g., `bookstore_db`
        *   `DATABASE_USER`: e.g., `bookstore_user`
        *   `DATABASE_PASSWORD`: **Choose a secure password** for the Django app's database user.
        *   `MYSQL_ROOT_PASSWORD`: **Choose a secure password** for the MySQL root user (used for initial DB setup within Docker).
        *   `DEBUG`: Set to `True` for development, `False` for production simulation.
        *   `DJANGO_ALLOWED_HOSTS`: e.g., `localhost 127.0.0.1 [::1] web` (include `web` if needed for container communication checks).
    *   **Example `.env` structure:**
        ```env
        SECRET_KEY='your_generated_secret_key_here'
        DEBUG=True
        DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1] web

        DATABASE_NAME=bookstore_db
        DATABASE_USER=bookstore_user
        DATABASE_PASSWORD=YourSecureDbPasswordHere!
        DATABASE_HOST=db # Service name from docker-compose.yml
        DATABASE_PORT=3306 # Internal MySQL port

        MYSQL_ROOT_PASSWORD=YourSecureRootPasswordHere!
        ```

3.  **Build and Start Containers:**
    Use Docker Compose to build the Django image (if it doesn't exist or if code changed) and start the `web` and `db` services.
    ```bash
    docker-compose up --build -d
    ```
    *   `--build`: Forces Docker to rebuild the `web` image based on the `Dockerfile`.
    *   `-d`: Runs the containers in detached mode (in the background).

4.  **Apply Database Migrations:**
    Once the containers are running (especially the database), execute the Django migrations inside the `web` container to create the necessary database tables.
    ```bash
    docker-compose exec web python manage.py migrate
    ```
    *(This will also run the data migration to seed initial books if configured).*

5.  **Create a Superuser (Admin Account):**
    Create an admin account to access the custom admin panel.
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```
    Follow the prompts to set a username, email, and password.

6.  **Access the Application:**
    Open your web browser and navigate to:
    *   **Homepage / Book List:** `http://localhost:8000/` or `http://localhost:8000/store/books/`
    *   **Admin Panel:** `http://localhost:8000/custom-admin/` (Log in with your superuser credentials via the standard Login page first).
    *   **Login:** `http://localhost:8000/accounts/login/`
    *   **Register:** `http://localhost:8000/accounts/register/`

## Docker Usage Notes

*   **Start Application:** `docker-compose up -d`
*   **Start with Rebuild:** `docker-compose up --build -d`
*   **Stop Application:** `docker-compose down` (stops and removes containers/network)
*   **Stop Temporarily:** `docker-compose stop` (stops containers without removing)
*   **Restart Stopped Containers:** `docker-compose start`
*   **View Logs:** `docker-compose logs -f` (follow logs) or `docker-compose logs web` (logs for specific service)
*   **View Running Services:** `docker-compose ps`
*   **Run Management Commands:** `docker-compose exec web python manage.py <command>` (e.g., `migrate`, `createsuperuser`, `shell`)
*   **Force Rebuild without Cache:** `docker-compose build --no-cache web`
*   **Reset Database (Deletes ALL Data):**
    ```bash
    docker-compose down
    docker volume rm <your_project_directory_name>_mysql_data # Find name via 'docker volume ls'
    docker-compose up -d --build
    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py createsuperuser
    ```

## Jenkins Usage Notes

*   The `Jenkinsfile` in the repository root outlines a declarative pipeline for Continuous Integration and Continuous Deployment (CI/CD).
*   **Pipeline Stages (Example):**
    1.  `Checkout`: Fetches the source code from the Git repository.
    2.  `Lint & Security Check (Optional)`: Placeholder for running tools like Flake8 or Bandit.
    3.  `Build Docker Image`: Builds the `web` application image using `docker build` or `docker-compose build`.
    4.  `Unit Tests (Example)`: Placeholder demonstrating how to run Django tests (`manage.py test`) inside a container, potentially linking to the `db` service.
    5.  `Push Docker Image (Optional)`: Pushes the built image to a container registry (like Docker Hub). Requires registry credentials configured in Jenkins.
    6.  `Deploy & Migrate`: Deploys the application using `docker-compose up` on the target server and runs database migrations (`manage.py migrate`) via `docker-compose exec`.
*   **Setup Required:**
    *   A running Jenkins server with necessary plugins (Docker, Pipeline, Git, Credentials Binding, etc.).
    *   Jenkins agent(s) configured with Docker and Docker Compose installed.
    *   Configuration of credentials within Jenkins (e.g., for Git, Docker Hub, `.env` secrets if not handled externally).
    *   A Jenkins Pipeline job configured to use the `Jenkinsfile` from SCM (Source Control Management).
*   **Note:** The provided `Jenkinsfile` is a template. Specific commands, environment variable handling (especially secrets), deployment targets (e.g., SSH to a server), and waiting logic (e.g., for DB health) might need adjustment based on your actual Jenkins setup and deployment environment.

## Project Structure

```
bookstore-django-project/
├── accounts/             # Django app for user authentication (views, urls)
├── admin_panel/          # Django app for the custom admin interface (views, urls, mixins)
├── bookstore_project/    # Main Django project settings (settings.py, urls.py, wsgi.py)
├── store/                # Django app for core store logic (models, views, urls, context_processors)
│   └── migrations/       # Database migration files for store app
├── static/               # Project-wide static files (CSS, JS, images)
│   └── css/
│       └── style.css
├── templates/            # Project-wide templates
│   ├── accounts/
│   ├── admin_panel/
│   ├── base/
│   └── store/
├── venv/                 # Virtual environment (Included in .gitignore)
├── .env                  # Environment variables (MUST NOT be committed - use .env.example)
├── .gitignore            # Specifies intentionally untracked files for Git
├── Dockerfile            # Instructions to build the Django application Docker image
├── docker-compose.yml    # Defines services (web, db) for Docker Compose
├── Jenkinsfile           # Declarative pipeline script for Jenkins CI/CD
├── manage.py             # Django's command-line utility
├── requirements.txt      # Python package dependencies
└── README.md             # This file
```

## Troubleshooting

*   **DB Connection Error (Access Denied):** Double-check `DATABASE_PASSWORD` in `.env` matches the password used when the DB container was first created. If unsure, reset the DB volume (see Docker Usage Notes).
*   **DB Connection Error (Unknown Host 'db'):** Ensure you are running the app via `docker-compose up`. If running `manage.py runserver` locally, change `DATABASE_HOST` in `.env` to `127.0.0.1` and `DATABASE_PORT` to the *mapped* port (e.g., `3307`).
*   **Table Doesn't Exist:** Run `docker-compose exec web python manage.py migrate`.
*   **Static Files (CSS/JS) Not Loading (404):**
    *   Ensure `DEBUG=True` in `.env`.
    *   Verify `STATIC_URL` and `STATICFILES_DIRS` in `settings.py`.
    *   Check the volume mount `.:/app` in `docker-compose.yml`.
    *   Clear browser cache (hard refresh).
    *   Check Browser Developer Console (F12 -> Network/Console) for errors.
*   **TemplateSyntaxError ('static' tag):** Add `{% load static %}` at the top of the template file (e.g., `base.html`).
*   **Emoji/Character Error (Incorrect string value):** Ensure the database/table/column uses `utf8mb4` character set. Best fixed by adding `command: [--character-set-server=utf8mb4, --collation-server=utf8mb4_unicode_ci]` to the `db` service in `docker-compose.yml` and resetting the DB volume.

---
