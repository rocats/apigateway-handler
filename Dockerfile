#                      _       
#   _ __ ___   ___ __ _| |_ ___ 
#  | '__/ _ \ / __/ _` | __/ __|
#  | | | (_) | (_| (_| | |_\__ \
#  |_|  \___/ \___\__,_|\__|___/
#
#  https://github.com/rocats/apigateway-interceptor
#
#  Copyright (C) 2023 @rocats
#
#  This is a self-hosted software, liscensed under the Apache License. 
#  See /License for more information.

ARG APP_DIR="/app"

### BUILDER ###
FROM cgr.dev/chainguard/python:latest-dev as builder

ARG APP_DIR

ENV LANG=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="${APP_DIR}/venv/bin:$PATH"

WORKDIR ${APP_DIR}

RUN python -m venv venv
ADD requirements.prod.txt ${APP_DIR}/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

### PROD ###
FROM cgr.dev/chainguard/python:latest as prod

ARG APP_DIR

ENV PYTHONUNBUFFERED=1 \
    PATH="${APP_DIR}/venv/bin:$PATH"

WORKDIR ${APP_DIR}

COPY --from=builder ${APP_DIR}/venv ./venv
COPY src/ ./

ENTRYPOINT [ "python" ]
CMD [ "index.py" ]
