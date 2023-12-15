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
ARG APP_DIR="/app"

FROM python:${PYTHON_VERSION}-bullseye as builder

ARG APP_DIR

ADD requirements.prod.txt ${APP_DIR}/requirements.txt

WORKDIR ${APP_DIR}
RUN pip install -r requirements.txt

COPY src/ ./

RUN pyinstaller index.py

# === Prod Stage === #
FROM debian:bullseye-slim as prod

ARG APP_DIR

RUN apt update -y && \
    apt-get install -y --no-install-recommends \
    ca-certificates

RUN apt-get clean autoclean && \
    apt-get autoremove -y && \
    rm -rf /var/lib/{apt,dpkg,cache,log}/

WORKDIR ${APP_DIR}

COPY --from=builder ${APP_DIR}/dist/index/ ./

RUN chmod +x ./index

CMD ["./index"]
