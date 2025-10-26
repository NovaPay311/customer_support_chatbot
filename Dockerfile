# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Gunicorn and any needed packages specified in requirements.txt
# Gunicorn is explicitly installed here to ensure it is available for the CMD
RUN pip install --no-cache-dir gunicorn -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run gunicorn to serve the Flask application
# The command is: gunicorn --bind 0.0.0.0:5000 src.app:app
# We use 4 worker processes for better performance and robustness.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "src.app:app"]
