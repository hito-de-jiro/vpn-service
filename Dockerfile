# pull official base image
FROM python:3.9-alpine3.16

COPY requirements.txt /temp/requirements.txt
# copy project
COPY app /app
# set work directory
WORKDIR /app
EXPOSE 8000
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install dependencies
RUN python -m pip install --upgrade pip
RUN pip install -r /temp/requirements.txt
RUN adduser --disabled-password service-user
USER service-user
