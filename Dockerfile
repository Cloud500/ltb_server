FROM python:3.9-alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
EXPOSE 8000

RUN apk update \
  && apk add postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib-dev libjpeg curl

RUN mkdir /config
ADD requirements.txt /config/
RUN pip install --upgrade pip
RUN pip install -r /config/requirements.txt

ADD config/fetch_next_book.sh /etc/periodic/15min/fetch_next_book.sh


RUN mkdir /src

COPY config/entrypoint.sh /src/
RUN chmod +x /src/entrypoint.sh

ADD manage.py /src/
ADD ltb_server /src/ltb_server
ADD ltb /src/ltb
ADD stock /src/stock
ADD api /src/api

ADD static /src/static
ADD templates /src/templates
RUN mkdir /src/media
RUN mkdir /src/media/cover

WORKDIR /src
#CMD ["manage.py", "runserver", "0.0.0.0:8000"]
#ENTRYPOINT ["python"]
ENTRYPOINT ["/src/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]