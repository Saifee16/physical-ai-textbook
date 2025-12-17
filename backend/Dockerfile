# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt from the same folder
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app folder
COPY ./app ./app

# Expose port 8000
EXPOSE 8000

# Run Uvicorn server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

