FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the Python script into the container
COPY freibad_metric.py .

# Install the required dependencies
RUN pip install requests prometheus_client

# Command to run the application
CMD ["python", "freibad_metric.py"]