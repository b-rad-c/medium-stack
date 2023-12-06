FROM python:3.12.0-alpine3.18

# app
WORKDIR /app
COPY ./samples /app/samples/
COPY ./medium-stack /app/medium-stack/
COPY ./pytest.ini /app/

# deps
RUN apk add mediainfo 
RUN pip install --upgrade pip
RUN pip install -e ./medium-stack/mstack

# dev deps
RUN pip install -r medium-stack/requirements-dev.txt

# run
EXPOSE 8000
WORKDIR /app/medium-stack/
CMD ["/bin/sh", "dev.sh"]