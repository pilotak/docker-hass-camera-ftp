FROM python:3-alpine

WORKDIR /app

COPY . /app

RUN apk add zlib-dev jpeg-dev gcc musl-dev \
    && pip3 install --trusted-host pypi.python.org -r requirements.txt

CMD ["python3", "-u", "index.py"]