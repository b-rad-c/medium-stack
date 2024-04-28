# vars :: {"sample_app":"package_name"}
FROM python:3.12.0-alpine3.18

WORKDIR /app

# deps
RUN apk add mediainfo
# https://stackoverflow.com/a/72600944
RUN apk add --virtual .tmp-build-deps build-base gcc python3-dev musl-dev libffi-dev openssl-dev  
RUN pip install --upgrade pip

# mstack
COPY ./samples /app/samples/
# replace the below with a git clone, eventually to be replaced with a pip install
COPY ./medium-stack /app/medium-stack/
COPY ./pytest.ini /app/

RUN pip install -e ./medium-stack/mstack
RUN pip install -r medium-stack/requirements-dev.txt

# delete temp deps
RUN apk del .tmp-build-deps

COPY ./sample_app/dist /app/sample_app
RUN pip install -e /app/sample_app

# run
EXPOSE 8000
WORKDIR /app/sample_app
CMD ["/bin/sh", "web.sh"]