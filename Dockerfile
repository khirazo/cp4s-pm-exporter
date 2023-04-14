# docker image build -t cp4s-pm-exporter:1.0.0 .
# docker run -p 5000:5000 -d cp4s-pm-exporter:1.0.0

# Base image using Red Hat UBI8 for python 3.8
FROM registry.access.redhat.com/ubi8/python-38:latest

ARG APP_USER_NAME=appuser
ENV APP_ROOT /opt/app-root

# root privilege
USER 0
RUN yum install -y cronie sudo

RUN useradd -l $APP_USER_NAME && \
echo -e "appuser ALL=(ALL) NOPASSWD:ALL\n" >> /etc/sudoers && \
visudo -cf /etc/sudoers

COPY ./crontab.txt $APP_ROOT/
RUN crontab -u $APP_USER_NAME $APP_ROOT/crontab.txt

COPY ./startup.sh $APP_ROOT/
RUN chmod 755 $APP_ROOT/startup.sh

WORKDIR $APP_ROOT/app
COPY ./app $APP_ROOT/app
RUN chmod -R 755 $APP_ROOT/app

WORKDIR $APP_ROOT/store
COPY ./store/config.yml $APP_ROOT/store/
RUN chmod -R 755 $APP_ROOT/store
RUN chmod 777 $APP_ROOT/store

WORKDIR $APP_ROOT/store/log
RUN chmod 777 $APP_ROOT/store/log
RUN touch $APP_ROOT/store/log/app.log
RUN chmod 666 $APP_ROOT/store/log/app.log

# Update to the latest pip
RUN pip install --upgrade pip
# Install wheel
RUN pip install wheel
# Install Flask, urllib3, etc
RUN pip install Flask urllib3 PyYAML resilient

USER $APP_USER_NAME
WORKDIR $APP_ROOT/app
CMD ["/opt/app-root/startup.sh"]
