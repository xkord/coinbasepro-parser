FROM python:3.7

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

#ENV HOST 127.0.0.1

#ENV DATABASE coinbasepro
#ENV LOGIN coinbasepro
#ENV PASSWORD coinbasepro_password
#ENV HOST localhost

ENV ORDER_LEVEL 3
ENV ORDERS 1
#ENV TRADES 1
#ENV FROM_TIME 1547751930
ENV TARGET BTC,ETH

#ENV RABBIT_HOST 127.0.0.1
#ENV RABBIT_EXCHANGE coinbasepro
#ENV RABBIT_LOGIN guest
#ENV RABBIT_PASSWORD guest

COPY . /opt/coinbasepro
COPY entrypoint.sh /opt/coinbasepro/entrypoint.sh
WORKDIR /opt/coinbasepro
RUN chmod +x entrypoint.sh

CMD bash entrypoint.sh
