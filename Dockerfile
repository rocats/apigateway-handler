#                      _       
#  _ __ ___   ___ __ _| |_ ___ 
# | '__/ _ \ / __/ _` | __/ __|
# | | | (_) | (_| (_| | |_\__ \
# |_|  \___/ \___\__,_|\__|___/
#
# https://github.com/rocats/apigateway-interceptor
#
#  Copyright (C) 2023 @rocats
#
#  This is a self-hosted software, liscensed under the Apache License. 
#  See /License for more information.

# === Build Stage === #
ARG PYTHON_VERSION

FROM python:${PYTHON_VERSION}-bullseye as builder

WORKDIR /app

ADD requirements.prod.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY src/ ./
RUN pyinstaller index.py

# === Prod Stage === #
FROM debian:bullseye-slim as prod

ARG PYTHON_VERSION

RUN apt update -y && \
    apt-get install -y --no-install-recommends \
    ca-certificates

RUN apt-get clean autoclean && \
    apt-get autoremove -y && \
    rm -rf /var/lib/{apt,dpkg,cache,log}/

WORKDIR /app

COPY --from=builder /app/dist/index/ ./

RUN chmod +x ./index

CMD ["./index"]
