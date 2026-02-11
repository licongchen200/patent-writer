# Use Python 3.11 slim image (stable and compatible)
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies (using only binary wheels to avoid build issues)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --only-binary=:all: -r requirements.txt || \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY main.py .
COPY enhance_patent.py .
COPY test_llm_proxy.py .

# Create output and input directories
RUN mkdir -p /app/output /app/input

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the patent writer
CMD ["python", "main.py"]
