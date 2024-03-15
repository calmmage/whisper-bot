# Start with the official Python image from the Docker Hub
FROM python:3.11-slim-buster

# Update and install FFmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get install -y build-essential

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install poetry and dependencies
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the command to start your bot
CMD ["python", "run.py"]
