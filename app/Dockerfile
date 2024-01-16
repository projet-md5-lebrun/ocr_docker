# Use an official Python runtime as a parent image
FROM python:3.9


# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
 
RUN apt-get update \
    && apt-get install -y libgl1-mesa-glx

EXPOSE 8000

# Run app.py when the container launches
CMD ["python", "app.py", "--host"]
