sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
pip install psycopg2

sudo -u postgres psql

CREATE DATABASE coinbasepro;
CREATE USER coinbasepro WITH password 'coinbasepro_password';
GRANT ALL privileges ON DATABASE coinbasepro TO coinbasepro;