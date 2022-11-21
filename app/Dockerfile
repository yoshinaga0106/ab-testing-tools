FROM python:3.10-slim

WORKDIR /

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY ./ /
RUN pip install poetry

# Install dependencies
RUN poetry install
