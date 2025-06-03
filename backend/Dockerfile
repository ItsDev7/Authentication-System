# Dockerfile
# This Dockerfile builds a Docker image for the backend FastAPI application.

# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# Use --no-cache-dir to prevent caching package data, which reduces image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
# The first '.' refers to the current directory on the host (where the Dockerfile is)
# The second '.' refers to the WORKDIR (/app) in the container
COPY . .

# Run the FastAPI application using Uvicorn
# Listen on all network interfaces (0.0.0.0) and port 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
