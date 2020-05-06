# Base python image
FROM python:3-slim-buster

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Setup working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Add requirements (to leverage Docker cache)
ADD ./requirements.txt /usr/src/app/requirements.txt

# Install requirements
RUN pip3 install -r requirements.txt

# Copy project
COPY . /usr/src/app