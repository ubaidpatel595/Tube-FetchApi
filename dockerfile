# Use an Alpine Linux-based image as the base
FROM python:3.9-alpine

# Install FFmpeg using the Alpine package manager
RUN apk --no-cache add ffmpeg

# Install build dependencies for psutil
RUN apk --no-cache add build-base python3-dev

# Set the FFMPEG environment variable to the FFmpeg binary path
ENV FFMPEG=ffmpeg

# Install any required Python packages
COPY requirements.txt /app/
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Flask app code into the image
COPY . /app

# Expose the port your Flask app will run on
EXPOSE 5000

# Start your Flask app
CMD ["python", "app.py"]
