# Use Python 3.12 as base image (CrewAI 1.15 supports 3.10-3.13)
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# API keys are NOT baked into the image: pass them at runtime with
#   docker run --env-file .env docker-crew

# Run the application
CMD ["python", "src/docker/main.py"] 