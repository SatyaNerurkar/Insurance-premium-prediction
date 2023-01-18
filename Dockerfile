# Use an official Python runtime as the base image
FROM python:3.8
# Define user as ROOT
USER root
# Create app directory
RUN mkdir /app
# Copy the application code
COPY . /app/
# Set the working directory
WORKDIR /app/
# Install the required packages
RUN pip3 install -r requirements.txt
# Expose port 5000 for the Flask application
EXPOSE 5000
# Set the command to start the application
CMD ["python", "app.py"]