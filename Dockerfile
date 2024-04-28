Dockerfile

From python:3

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir networkx pyyaml matplotlib
