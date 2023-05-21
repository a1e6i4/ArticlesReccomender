FROM python:3.8
WORKDIR /ArticlesReccomender
COPY . .

RUN apt-get update && \
    apt-get install -y --no-install-recommends libblas-dev liblapack-dev && \
    pip install --no-cache-dir numpy scipy surprise

RUN pip install -r /ArticlesReccomender/requirements.txt --no-cache-dir