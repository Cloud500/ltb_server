FROM python:3.9-alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
EXPOSE 8000

RUN mkdir /src \
  && mkdir /src/media \
  && mkdir /src/media/cover

COPY . /src/

RUN apk add --no-cache \
    libpq-dev \
    jpeg-dev \
    zlib-dev \
    libjpeg \
    curl \
  && apk add --no-cache --virtual .build-deps \
    python3-dev \
    gcc \
    musl-dev \
  && chmod +x /src/config/entrypoint.sh \
  && pip install --upgrade pip \
  && pip install --no-cache-dir -r /src/requirements.txt \
  && apk del .build-deps \
  && mv /src/config/fetch_next_book.sh /etc/periodic/daily/fetch_next_book.sh

WORKDIR /src
ENTRYPOINT ["/src/config/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]