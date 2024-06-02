# Use official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies and clean up to reduce image size
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libdrm2 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libnss3 \
    libnspr4 \
    curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Playwright and dependencies
RUN curl -fsSL https://playwright.dev/install.sh | bash && \
    playwright install && \
    playwright install-deps

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
