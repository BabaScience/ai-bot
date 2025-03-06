FROM python:3.12.7-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Environment variables set at runtime through docker-compose or docker run
ENV BOT_TOKEN=""
ENV DEFAULT_LANGUAGE="en"
ENV DEV="true"
ENV DEFAULT_MODEL="llama3.2"
ENV PYTHONUNBUFFERED=1

# Run the bot
CMD ["python", "bot.py"] 