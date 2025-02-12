FROM python:3.10.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip --progress-bar off
RUN apt-get update && apt-get upgrade -y

RUN mkdir /app
# Set working directory
WORKDIR /app
# Copy content into container
ADD . /app/

RUN pip install -r requirements.txt --progress-bar off