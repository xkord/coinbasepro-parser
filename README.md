# coinbasepro parser

Парсер coinbasepro

## Установка

### postgresql

```
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo -u postgres psql
```

### coinbasepro

```sh
virtualenv -p python3 venv
source venv/bin/activate
cd coinbasepro
pip install -r requirements.txt
python setup.py install
```

## Подготовка к использованию

### Создание базы данных

```
CREATE DATABASE coinbasepro;
CREATE USER coinbasepro WITH password 'YOUR_PASSWORD';
GRANT ALL privileges ON DATABASE coinbasepro TO coinbasepro;
```

## Использование

Необходимо задать переменные окружения для работы скрипта:

    	HOST = '127.0.0.1'
    	DATABASE = 'coinbasepro'
    	LOGIN = 'coinbasepro'
    	PASSWORD = 'coinbasepro_password'

    	# For rabbitmq
    	RABBIT_HOST = '127.0.0.1'
    	RABBIT_EXCHANGE = 'coinbasepro'
    	RABBIT_LOGIN = 'guest'
    	RABBIT_PASSWORD = 'guest'

    	ENV ORDER_LEVEL 2
    	ENV ORDERS 1
    	#ENV TRADES 1
    	#ENV FROM_TIME 1547751930
    	ENV TARGET BTC,ETH

```sh
python mq_server.py
```

```sh
# Help
coinbasepro -h
# VERBOSE mode with log file
coinbasepro -V -l log
```
