FROM python:3.6-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 23456

ENTRYPOINT ["python3"]

CMD ["-m", "swagger_server", "--email", "$FACEBOOK_EMAIL", "--password", "$FACEBOOK_PASSWORD", "--method", "facebok", "--library-build"]
