# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the service files to the working directory
COPY . .

# Expose the port on which the server will run
EXPOSE 50051

# Run the server
CMD ["python", "user_server.py"]