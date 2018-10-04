FROM python:3-alpine

#For cloning local git repo with docker container
RUN mkdir -p /app/work/salm_core

RUN apk update && apk add git

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 5005

CMD ["gunicorn", "--config", "gunicorn_config.py", "services:app"]
#CMD ["services.py"]