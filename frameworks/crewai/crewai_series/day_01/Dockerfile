# Use the official Python image
FROM python:3.11.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Don't bake API keys into the image: pass them at runtime instead, e.g.
#   docker run --env-file ../.env <image>

# Expose port 80 if your app will listen on it
EXPOSE 80

# Command to run your script
CMD ["python", "run_crew.py"]
