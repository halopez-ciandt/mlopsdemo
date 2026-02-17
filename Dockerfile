FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements-api.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements-api.txt

# Copy source code
COPY src/ src/
COPY models/ models/

# Set Python path
ENV PYTHONPATH=/app/src

# Train model if not exists
RUN python3 -m src.models.iris_model || echo "Model training failed, will train at runtime"

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start command
CMD ["python3", "-m", "uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]