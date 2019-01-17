import os
import time
import json
import logging
import pika
import cbpro
import time
import datetime
from dateutil.parser import parse
from coinbasepro.database import Database

logger = logging.getLogger("LOG")

e = os.environ.get


def rabbit_mq_send(all_info):
    if all([e('RABBIT_LOGIN'), e('RABBIT_PASSWORD'), e('RABBIT_HOST'), e('RABBIT_EXCHANGE')]):
        try:
            credentials = pika.PlainCredentials(e('RABBIT_LOGIN'), e('RABBIT_PASSWORD'))
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=e('RABBIT_HOST'),
                                                                           credentials=credentials))
            channel = connection.channel()

            channel.exchange_declare(exchange=e('RABBIT_EXCHANGE'), exchange_type='fanout')

            for info in all_info:
                channel.basic_publish(exchange=e('RABBIT_EXCHANGE'),
                                      routing_key='',
                                      body=json.dumps(info))
            connection.close()
        except Exception as error:
            logger.critical("Exception working with rabbitmq: %s", error)
    else:
        logger.critical("Please set ENV for rabbitmq")
        # exit(0)


def database_init():
    if all([e('DATABASE'), e('LOGIN'), e('HOST'), e('PASSWORD')]):
        db = Database(e('DATABASE'), e('LOGIN'), e('HOST'),
                      e('PASSWORD'))
        db.create_coinbasepro_orders_table()
        db.create_coinbasepro_trades_table()
        return db
    else:
        # logger.critical("Please set ENV for database")
        return None
        # exit(0)


class CoinbaseproScraper:

    def __init__(self):
        self.batch_dttm = time.time()
        self.database = database_init()
        self.pc = cbpro.PublicClient()

    def __enter__(self):
        self.start()

    def __exit__(self, type, value, traceback):
        pass

    def get_order(self, val):
        order_book = self.pc.get_product_order_book(val + '-USD', level=int(e('ORDER_LEVEL')))
        return order_book

    def get_trades(self, val):
        return self.pc.get_product_trades(product_id=val + '-USD')

    def start(self):
        from_time = None
        to_time = None
        target = None
        if e('FROM_TIME'):
            from_time = int(e('FROM_TIME'))
        else:
            from_time = int(time.time()) - 86400
        if e('TO_TIME'):
            to_time = int(e('TO_TIME'))
        if e('TARGET'):
            target = e('TARGET').replace(" ", "")
            targets = target.split(",")
            for target in targets:
                logger.info("Scraping %s", target)

                if e('ORDERS'):
                    logger.info("Starting to get orders for %s", target)
                    all_info = []
                    order = self.get_order(target)
                    base_asset = 'USD'
                    quote_asset = target
                    pair = base_asset + "-" + quote_asset
                    business_dttm = self.batch_dttm

                    for asks in order['asks']:
                        price = asks[0]
                        amount = asks[1]
                        id = asks[2]
                        order_type = 'ask'
                        result = {
                            "id": id,
                            "order_type": order_type,
                            "pair": pair,
                            "base_asset": base_asset,
                            "quote_asset": quote_asset,
                            "price": price,
                            "amount": amount,
                            "business_dttm": business_dttm
                        }
                        all_info.append(result)
                        print(result)
                    for bids in order['bids']:
                        price = bids[0]
                        amount = bids[1]
                        id = bids[2]
                        order_type = 'bid'
                        result = {
                            "id": id,
                            "order_type": order_type,
                            "pair": pair,
                            "base_asset": base_asset,
                            "quote_asset": quote_asset,
                            "price": price,
                            "amount": amount,
                            "business_dttm": business_dttm
                        }
                        all_info.append(result)
                        print(result)
                    if self.database:
                        for item in all_info:
                            self.database.insert_orders(item)
                    rabbit_mq_send(all_info)

                if e('TRADES'):
                    logger.info("Starting to get trades for %s", target)
                    trades = self.get_trades(target)

                    all_info = []
                    base_asset = 'USD'
                    quote_asset = target
                    pair = base_asset + "-" + quote_asset

                    for trade in trades:
                        id = trade['trade_id']
                        active_side = trade['side']
                        price = trade['price']
                        amount = trade['size']
                        business_dttm = trade['time']
                        time_obj = parse(business_dttm)
                        unixtime = int(time.mktime(time_obj.timetuple()))
                        # print(unixtime)
                        if unixtime < from_time:
                            break

                        result = {
                            "id": id,
                            "active_side": active_side,
                            "pair": pair,
                            "base_asset": base_asset,
                            "quote_asset": quote_asset,
                            "price": price,
                            "amount": amount,
                            "business_dttm": unixtime
                        }
                        all_info.append(result)
                        print(result)

                    if self.database:
                        for item in all_info:
                            self.database.insert_trades(item)
                    rabbit_mq_send(all_info)


if __name__ == '__main__':
    CoinbaseproScraper().start()
