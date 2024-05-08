# vars :: {"sample_app":"package_name"}
FROM python:3.12.0-alpine3.18

WORKDIR /app

# deps
RUN apk add mediainfo
# https://stackoverflow.com/a/72600944
RUN apk add --virtual .tmp-build-deps build-base gcc python3-dev musl-dev libffi-dev openssl-dev  
RUN pip install --upgrade pip

# install mstack
COPY ./medium-stack/samples /app/samples/
COPY ./medium-stack/pytest.ini /app/
COPY ./medium-stack/mbuilder/py/mbuilder /app/mbuilder

WORKDIR /app/mbuilder
RUN pip install -r requirements-dev.txt

# delete temp deps
RUN apk del .tmp-build-deps

COPY ./src/sample_app /app/sample_app
RUN pip install -e .

# install  sample_app

COPY . /app/sample_app
WORKDIR /app/sample_app
RUN pip install -e .

# run
EXPOSE 8000
CMD ["/bin/sh", "web.sh"]