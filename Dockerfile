# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install all needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8501 available to the world outside this container (Streamlit default)
EXPOSE 8501

# Command to run the Streamlit demo application
# This is the new entry point for the visual Demo MVP on Hugging Face Spaces.
CMD ["streamlit", "run", "src/app_demo.py", "--server.port=8501", "--server.address=0.0.0.0"]
