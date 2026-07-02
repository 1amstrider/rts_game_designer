# Dockerfile for Hugging Face Spaces
# Runtime: CPU (no GPU needed for this app)

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY . .

# Create necessary directories
RUN mkdir -p design data/images static templates

# Set environment variables (will be overridden by HF Spaces secrets)
ENV PYTHONUNBUFFERED=1
ENV PORT=7860

# Expose the port HF Spaces expects
EXPOSE 7860

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
