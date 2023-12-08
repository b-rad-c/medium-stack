FROM python:3.12.0-alpine3.18

WORKDIR /app

# deps
RUN apk add mediainfo
# https://stackoverflow.com/a/72600944
RUN apk add --virtual .tmp-build-deps build-base gcc python3-dev musl-dev libffi-dev openssl-dev  
RUN pip install --upgrade pip

# app
COPY ./samples /app/samples/
COPY ./medium-stack /app/medium-stack/
COPY ./pytest.ini /app/

RUN pip install -e ./medium-stack/mstack

# dev deps
RUN pip install -r medium-stack/requirements-dev.txt

# delete temp deps
RUN apk del .tmp-build-deps

# run
EXPOSE 8000
WORKDIR /app/medium-stack/
CMD ["/bin/sh", "dev.sh"]