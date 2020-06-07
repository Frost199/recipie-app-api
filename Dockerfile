# setup the python version alphine means a lightweight
FROM python:3.7-alpine

# maintainer
MAINTAINER Eleam Emmanuel

# run python in an unbuffered mode
ENV PYTHONUNBUFFERED 1

# copy requirements.txt and run pip install
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# make our app directory, switch to the app dir and
# make it our working directory and copy ./app to /app
RUN mkdir /app
WORKDIR /app
COPY ./app /app

# create a user that will run the application using docker
RUN adduser -D manny
USER manny
