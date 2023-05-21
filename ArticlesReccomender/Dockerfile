FROM python:3.9.7-slim
WORKDIR /ArticlesReccomender
COPY . .

RUN apt-get update && \
    apt-get install -y --no-install-recommends libblas-dev liblapack-dev && \
    pip install --no-cache-dir numpy scipy surprise

RUN pip install -r /ArticlesReccomender/requirements.txt --no-cache-dir