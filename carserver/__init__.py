from flask import Flask
from influxdb import InfluxDBClient

app = Flask(__name__)

app.config['SECRET_KEY']='Th1s1ss3cr3t'

# --------
# database
# export: client
# --------
database_name = 'DriveS'

client = InfluxDBClient('localhost', 8086, 'root', 'root', database_name)
client.create_database(database_name)


# -------------
# router config
# -------------
from carserver import router
