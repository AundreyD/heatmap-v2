import json
import server
import os
from sqlite3 import Connection as SQLite3Connection
from sqlalchemy import event
from sqlalchemy.engine import Engine
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import dask.dataframe as dd


# file path
dirname = os.path.dirname(__file__)

# app
app = Flask(__name__)

# config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlitedb.file"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = 0

db = SQLAlchemy(app)

ipv4_csv_file = os.path.join(dirname, 'GeoLite2-City-Blocks-IPv4.csv')
ipv6_csv_file = os.path.join(dirname, 'GeoLite2-City-Blocks-IPv6.csv')
ipv4 = dd.read_csv(ipv4_csv_file, dtype={
    "network" : str,
    "geoname_id" : str,
    "registered_country_geoname_id" : str,
    "represented_country_geoname_id" : str,
    "is_anonymous_proxy" : str,
    "is_satellite_provider" : str,
    "postal_code" : str,
    "latitude" : str,
    "longitude" : str,
    "accuracy_radius" : str,
})
ipv4 = ipv4.drop(['network', 'accuracy_radius','is_satellite_provider'
,'is_anonymous_proxy', 'represented_country_geoname_id',
'registered_country_geoname_id', 'postal_code' ], axis=1)
ipv6 = dd.read_csv(ipv6_csv_file, dtype={
    "network" : str,
    "geoname_id" : str,
    "registered_country_geoname_id" : str,
    "represented_country_geoname_id" : str,
    "is_anonymous_proxy" : str,
    "is_satellite_provider" : str,
    "postal_code" : str,
    "latitude" : str,
    "longitude" : str,
    "accuracy_radius" : str,
})
ipv6 = ipv6.drop(['network', 'accuracy_radius','is_satellite_provider'
,'is_anonymous_proxy', 'represented_country_geoname_id',
'registered_country_geoname_id', 'postal_code' ], axis=1)

ipv4data = [ipv4.compute().to_json('temp.json', orient='records', lines=True)]


print('ip data', ipv4data)
