FROM python:3.12.0-alpine3.18

WORKDIR /app

RUN apk add mediainfo
# https://stackoverflow.com/a/72600944
RUN apk add --virtual .tmp-build-deps build-base gcc python3-dev musl-dev libffi-dev openssl-dev
RUN pip install --upgrade pip

#
# mstack
#

COPY ./samples /app/samples
COPY ./mbuilder /app/mbuilder
COPY ./pytest.ini /app


WORKDIR /app/mbuilder/py/mbuilder/
RUN pip install -r requirements-dev.txt
RUN pip install -e ./src/mtemplate/app

# delete temp deps
RUN apk del .tmp-build-deps

#
# app
#

EXPOSE 8000
WORKDIR /app/mbuilder/py/mbuilder/src/mtemplate/app

CMD ["/bin/sh", "web.sh"]