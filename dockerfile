# Stage 1: Build dependencies in a lightweight environment
FROM python:3.12-alpine AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/dependencies -r requirements.txt

# Stage 2: Minimal final image
FROM alpine:latest

WORKDIR /app

# Install only Python runtime
RUN apk add --no-cache python3

# Copy dependencies from the builder stage
COPY --from=builder /dependencies /usr/local

# Copy the application code
COPY . .

# Set Python path
ENV PYTHONPATH=/usr/local

# Use a non-root user
RUN adduser -D appuser
USER appuser

ENTRYPOINT ["python3"]
CMD ["app.py"]
