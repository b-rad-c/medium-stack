FROM python:3.12.0-alpine3.18

# app
WORKDIR /app
COPY ./medium-stack /app/

# deps
RUN apk add mediainfo 
RUN pip install --upgrade pip
RUN pip install -e mstack

# dev deps
RUN pip install -r requirements-dev.txt

# run
EXPOSE 8000
CMD ["/bin/sh", "dev.sh"]