# Use official lightweight Python image
FROM python:3.9-slim

# Set working directory in container
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y gcc libffi-dev

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project source
COPY . .

# Expose Flask default port
EXPOSE 5000

# Default command to run Flask app
CMD ["python", "run.py"]
