# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0
RUN apt-get -y install tesseract-ocr
# Upgrade pip and setuptools
RUN pip install --upgrade pip setuptools

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which your application will run
EXPOSE 8000

# Set the environment variable to disable parallelism
ENV TOKENIZERS_PARALLELISM=false

# Specify the command to run on container startup
CMD ["python", "app.py"]
