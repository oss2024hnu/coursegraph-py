From python:3

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir networkx pyyaml matplotlib

# if you want to run python code 
# docker container exec -it [docker ID] python3 concept-demo.py
