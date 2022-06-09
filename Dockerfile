FROM python:3.8-slim-buster

RUN apt-get update && apt-get -y install cron gcc libmariadb-dev

WORKDIR /banktransactioncollect

COPY . .

RUN pip3 install -r requirements.txt

COPY crontab /etc/cron.d/crontab

RUN chmod 0644 /etc/cron.d/crontab

RUN /usr/bin/crontab /etc/cron.d/crontab

CMD ["cron", "-f"]
