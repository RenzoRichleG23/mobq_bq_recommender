# Use the official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY . .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script file to the container
COPY main.py .

# Run the Python script
CMD ["python", "main.py"]
