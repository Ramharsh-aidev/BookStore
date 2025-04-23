# Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for mysqlclient and potentially other packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gcc \
       default-libmysqlclient-dev \
       pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install pipenv (or just use requirements.txt)
# RUN pip install pipenv

# Copy the requirements file into the container
COPY requirements.txt /app/
# COPY Pipfile Pipfile.lock /app/ # If using pipenv

# Install any needed packages specified in requirements.txt
RUN pip install --default-timeout=100 --no-cache-dir -r requirements.txt
# RUN pipenv install --system --deploy --ignore-pipfile # If using pipenv

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose port 8000 to allow communication to/from server
EXPOSE 8000

# Command to run the application using Gunicorn
# Adjust workers based on your server resources
# Use 0.0.0.0 to accept connections from any IP (necessary inside Docker)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "bookstore_project.wsgi:application"]