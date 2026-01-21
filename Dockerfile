FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies (needed for some python packages)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from the specific module location
COPY Milestone_3/Module_5_Flask_Backend_API/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project structure
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose the port (Hugging Face usually uses 7860)
EXPOSE 7860

# Command to run the application
# Note: We need to change the working directory or adjust the python path
WORKDIR /app/Milestone_3/Module_5_Flask_Backend_API

# Run with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "--workers", "1", "--timeout", "120", "run:app"]
