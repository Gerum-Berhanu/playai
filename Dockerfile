# Use official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install Playwright and necessary dependencies
RUN apt-get update && apt-get install -y libatk-bridge2.0-0 libgtk-3-0 libdrm2 libxdamage1 libxrandr2 libgbm1 libasound2
RUN playwright install

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]