# Use official Python slim image
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Expose port
EXPOSE 5000

# Use gunicorn for production-like run
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
