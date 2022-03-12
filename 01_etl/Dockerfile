FROM ubuntu
COPY . /root
WORKDIR /root/
RUN apt-get update && apt-get -y install cron
RUN apt-get install -y python3.8 && apt-get install -y python3-pip
RUN pip install -r requirements.txt
RUN chmod 0644 crontab
RUN crontab crontab
RUN touch /var/log/cron.log
CMD cron && tail -f /var/log/cron.log
