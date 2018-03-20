FROM python:3
ADD . /alert_service
WORKDIR /alert_service
RUN python setup.py install
CMD [ "alerter" ]