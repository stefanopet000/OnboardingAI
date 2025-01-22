# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for torch
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Environment variables (replace these with your actual values when running)
ENV SLACK_BOT_TOKEN=""
ENV SLACK_APP_TOKEN=""

# Command to run the application
CMD ["python", "slack_bot.py"]