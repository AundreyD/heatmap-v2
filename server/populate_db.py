import json
# import server
import os
import sqlite3
from sqlite3 import Connection as SQLite3Connection
from sqlalchemy import event
from sqlalchemy.engine import Engine
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import dask.dataframe as dd
from dask.diagnostics import ProgressBar
pbar = ProgressBar()
pbar.register()


# file path
dirname = os.path.dirname(__file__)

# app
app = Flask(__name__)

# config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = 0

db = SQLAlchemy(app)



class GeoData(db.Model):
    __tablename__ = 'geodata'
    id = db.Column(db.String(10), primary_key=True)
    ip = db.Column(db.String(4))
    latitude = db.Column(db.String(10))
    longitude = db.Column(db.String(10))

db.create_all()

ipv4_csv_file = os.path.join(dirname, 'GeoLite2-City-Blocks-IPv4.csv')
ipv6_csv_file = os.path.join(dirname, 'GeoLite2-City-Blocks-IPv6.csv')
ipv4 = pd.read_csv(ipv4_csv_file, dtype={
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
ipv4 = ipv4.drop(['geoname_id', 'accuracy_radius','is_satellite_provider'
,'is_anonymous_proxy', 'represented_country_geoname_id',
'registered_country_geoname_id', 'postal_code' ], axis=1)
ipv6 = pd.read_csv(ipv6_csv_file, dtype={
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
ipv6 = ipv6.drop(['geoname_id', 'accuracy_radius','is_satellite_provider'
,'is_anonymous_proxy', 'represented_country_geoname_id',
'registered_country_geoname_id', 'postal_code' ], axis=1)

ipv4data = ipv4.to_dict('records')
ipv6data = ipv6.to_dict('records')
frames = [ipv4, ipv6]
result = pd.concat(frames)
combined_data = ipv4data + ipv6data

result.to_sql(name='geodata', con="sqlite:///database.db",  if_exists="replace", index=False)
# ipv6.to_sql(name='geodata', con="sqlite:///database.db",  if_exists="replace", index=False)



# for key in ipv6data:
#     new_geodata = GeoData( ip='ipv6', geoname_id=key['geoname_id'], latitude=key['latitude'], longitude=key['longitude'])
#     db.session.merge(new_geodata)
#     db.session.commit()

# for key in ipv4data:
#     print(key['geoname_id'])