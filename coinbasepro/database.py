import psycopg2
from psycopg2 import sql
import logging

logger = logging.getLogger("LOG")


class Database:

    def __init__(self, database, user, host, password):
        self.database = database
        self.user = user
        self.host = host
        self.password = password
        self.conn = None
        self.cur = None
        self.connect()
        self.coinbasepro_orders_table = "coinbasepro_orders"
        self.coinbasepro_trades_table = "coinbasepro_trades"

        # self.drop_coinbasepro_orders_table()

    def __enter__(self):
        pass

    def __exit__(self, exit_type, value, traceback):
        pass

    def connect(self):
        self.conn = psycopg2.connect(database=self.database, user=self.user,
                                     host=self.host, password=self.password)
        self.cur = self.conn.cursor()

    def is_table_exists(self, table_name):
        if self.conn.closed != 0:
            self.connect()
        self.cur.execute("SELECT exists(SELECT * FROM information_schema.tables "
                         "WHERE table_name=%s)", (table_name,))
        return self.cur.fetchone()[0]

    def create_coinbasepro_orders_table(self):
        if self.is_table_exists(self.coinbasepro_orders_table):
            logger.info("Table already exists")
            return
        command = ("""
        CREATE TABLE """ + self.coinbasepro_orders_table + """ 
        (
            pid SERIAL PRIMARY KEY,
            id TEXT,
            order_type TEXT,
            pair TEXT,
            base_asset TEXT,
            quote_asset TEXT,
            price FLOAT,
            amount FLOAT,
            business_dttm INTEGER
        )
        """)
        if self.conn.closed != 0:
            self.connect()
        self.cur.execute(command)
        self.conn.commit()

    def create_coinbasepro_trades_table(self):
        if self.is_table_exists(self.coinbasepro_trades_table):
            logger.info("Table already exists")
            return
        command = ("""
        CREATE TABLE """ + self.coinbasepro_trades_table + """ 
        (
            pid SERIAL PRIMARY KEY,
            id TEXT,
            active_side TEXT,
            pair TEXT,
            base_asset TEXT,
            quote_asset TEXT,
            price FLOAT,
            amount FLOAT,
            business_dttm INTEGER
        )
        """)
        if self.conn.closed != 0:
            self.connect()
        self.cur.execute(command)
        self.conn.commit()

    def drop_table(self, table_name):
        if self.conn.closed != 0:
            self.connect()
        self.cur.execute('DROP TABLE "' + table_name + '";')
        self.conn.commit()

    def drop_coinbasepro_orders_table(self):
        self.drop_table(self.coinbasepro_orders_table)

    def drop_coinbasepro_trades_table(self):
        self.drop_table(self.coinbasepro_trades_table)

    def close_connection(self):
        self.cur.close()
        self.conn.close()

    def insert_orders(self, info):
        try:
            if self.conn.closed != 0:
                self.connect()
            self.cur.execute(sql.SQL(
                "INSERT INTO {} (id, order_type, pair, base_asset, quote_asset, price, amount, business_dttm) VALUES \
                (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING")
                             .format(sql.Identifier(self.coinbasepro_orders_table)),
                             [info['id'], info['order_type'], info['pair'], info['base_asset'], info['quote_asset'],
                              info['price'], info['amount'],
                              info['business_dttm']])
            self.conn.commit()

            return True
        except Exception as e:
            self.conn.rollback()
            logger.critical("Exception: %s", e)
            return False

    def insert_trades(self, info):
        try:
            if self.conn.closed != 0:
                self.connect()
            self.cur.execute(sql.SQL(
                "INSERT INTO {} (id, active_side, pair, base_asset, quote_asset, price, amount, business_dttm) VALUES \
                (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING")
                             .format(sql.Identifier(self.coinbasepro_trades_table)),
                             [info['id'], info['active_side'], info['pair'], info['base_asset'], info['quote_asset'],
                              info['price'], info['amount'],
                              info['business_dttm']])
            self.conn.commit()

            return True
        except Exception as e:
            self.conn.rollback()
            logger.critical("Exception: %s", e)
            return False

