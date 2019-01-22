FROM python:3.6-alpine as builder

RUN apk update && apk add build-base postgresql-dev python-dev
RUN mkdir /install

COPY requirements.txt /requirements.pip
WORKDIR /

RUN pip install --prefix=/install -r /requirements.pip
RUN  ls /install

FROM python:3.6-alpine
RUN apk update && apk add postgresql-dev libffi-dev zlib-dev jpeg-dev bash
COPY --from=builder /install /usr/local

#ENV HOST 127.0.0.1

#ENV DATABASE coinbasepro
#ENV LOGIN coinbasepro
#ENV PASSWORD coinbasepro_password
#ENV HOST localhost

ENV ORDER_LEVEL 2
ENV ORDERS 1
#ENV TRADES 1
#ENV FROM_TIME 1547751930
ENV TARGET BTC,ETH

#ENV RABBIT_HOST 127.0.0.1
#ENV RABBIT_EXCHANGE coinbasepro
#ENV RABBIT_LOGIN guest
#ENV RABBIT_PASSWORD guest

COPY ./coinbasepro /opt/application/coinbasepro
COPY entrypoint.sh /opt/application
COPY setup.py /opt/application
WORKDIR /opt/application

RUN chmod +x entrypoint.sh
CMD bash entrypoint.sh
