# Use the official Python image as the base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the bot's source code to the container's working directory
COPY run.py web_scarpping.py /app/

# Install the required Python packages
RUN python -m pip install --no-cache-dir python-telegram-bot==13.7 requests==2.31.0 bs4==0.0.1

# Start the bot when the container runs
CMD ["python", "run.py"]
