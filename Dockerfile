# Use an official Python runtime as a parent image
FROM python:3.9

# Install ffmpeg for audio processing
RUN apt-get update && apt-get install -y ffmpeg

# Set the working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Run the bot
CMD ["python", "your_bot_file.py"]
