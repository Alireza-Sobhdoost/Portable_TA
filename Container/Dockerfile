# Use a lightweight Python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install system dependencies (optional, uncomment if you need)
# RUN apt-get update && apt-get install -y build-essential

# Copy only requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose a port IF your app runs as a server (change to yours)
EXPOSE 9000

# Run your main script
CMD ["python", "openai_api.py"]
