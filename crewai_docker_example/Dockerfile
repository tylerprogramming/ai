# Use Python 3.11.9 as base image
FROM python:3.11.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the .env file if it’s used for environment variables
COPY .env .env

# Run the application
CMD ["python", "src/docker/main.py"] 