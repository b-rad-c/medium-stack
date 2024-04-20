FROM python:3.12.0-alpine3.18

ARG DEVELOPMENT_MODE=false

WORKDIR /app

RUN apk add mediainfo
# https://stackoverflow.com/a/72600944
RUN apk add --virtual .tmp-build-deps build-base gcc python3-dev musl-dev libffi-dev openssl-dev
RUN python -m venv .venv --upgrade-deps --prompt "(mstack)"
RUN source .venv/bin/activate 

#
# mstack
#

COPY ./samples /app/samples/
COPY ./medium-stack /app/medium-stack/
COPY ./pytest.ini /app/

# if development mode
RUN if [ "$DEVELOPMENT_MODE" = "true" ]; then \
    echo ":: -> development mode"; \
    pip install -e ./medium-stack/mstack && pip install -r medium-stack/requirements-dev.txt; \
    exit $?; \
    fi

RUN if [ "$DEVELOPMENT_MODE" = "false" ]; then \
echo ":: -> production mode"; \
    pip install ./medium-stack/mstack; \
    exit $?; \
    fi

# delete temp deps
RUN apk del .tmp-build-deps

#
# app
#

EXPOSE 8000
WORKDIR /app/medium-stack/mstack/src/mtemplate/app

RUN pip install -e .

CMD ["/bin/sh", "web.sh"]