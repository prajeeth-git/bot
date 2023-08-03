# Use the official Python image as the base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the bot's source code to the container's working directory
COPY run.py web_scarpping.py secret.py /app/

# Install the required Python packages
RUN python -m pip install --no-cache-dir package1 package2 package3

# Start the bot when the container runs
CMD ["python", "run.py"]
