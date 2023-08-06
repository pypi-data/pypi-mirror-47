ARG PYTHON_VERSION=3.7
FROM python:${PYTHON_VERSION}-alpine

WORKDIR /app

RUN apk add --update make git
RUN pip install --upgrade setuptools pip
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . ./
