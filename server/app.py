from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import os
import pandas as pd
import json
import dask.dataframe as dd

app = Flask(__name__, static_folder='../map/dist', static_url_path='/')

cors = CORS(app)
dirname = os.path.dirname(__file__)
app.config['CORS_HEADERS'] = 'Content-Type'

zf = ZipFile( os.path.join(dirname, 'csv.zip'))


ipv4 = pd.read_csv(zf.open('GeoLite2-City-Blocks-IPv4.csv'),chunksize=2000, dtype={
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
ipv4 = ipv4.drop(['accuracy_radius','is_satellite_provider'
,'is_anonymous_proxy', 'represented_country_geoname_id',
'registered_country_geoname_id', 'postal_code' ], axis=1)
ipv6 = pd.read_csv(zf.open('GeoLite2-City-Blocks-IPv6.csv'), chunksize=2000, dtype={
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

ipv6 = ipv6.drop([ 'accuracy_radius','is_satellite_provider'
,'is_anonymous_proxy', 'represented_country_geoname_id',
'registered_country_geoname_id', 'postal_code' ], axis=1)

@app.route('/', methods=['GET'])
def root():
    return app.send_static_file('index.html') 

@app.route('/api/data', methods=['Get'])
@cross_origin()
def coords():
    args = request.args
    ip_type = args['type']
    north = args['north']
    east = args['east']
    south = args['south']
    west = args['west']

    if(ip_type == 'ipv6'):
        return_data = ipv6[(south <= ipv6['latitude']) & (north >=ipv6['latitude']) & (west >= ipv6['longitude']) & (east <= ipv6['longitude'])]
    else:
        return_data = ipv4[(south <= ipv4['latitude']) & (north >=ipv4['latitude']) & (west >= ipv4['longitude']) & (east <= ipv4['longitude'])]



    return return_data.to_json(orient='records')



if __name__ == '__main__':
    app.run(debug=True)