# Use a lightweight Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the .env file and the bot code into the container
COPY . .

# Command to run your bot script
CMD ["python", "test_L_1.py"]
