from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import os
import pandas as pd
import json
import dask.dataframe as dd

app = Flask(__name__)
cors = CORS(app)
dirname = os.path.dirname(__file__)
app.config['CORS_HEADERS'] = 'Content-Type'

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
# ipv4.sort_values(by=['latitude'])
# ipv6.sort_values(by=['latitude'])
conn = sqlite3.connect('database.db')
print ("Opened database successfully")



@app.route('/api/data', methods=['Get'])
# @cross_origin()
def test():
    args = request.args
    # ip_type = args['type']
    east = args['ne_lat']
    west = args['sw_lat']
    north = args['ne_long']
    south = args['sw_long']
    print(args)
    
    lat = ipv4['latitude']
    lon = ipv4['longitude']
    dataa = ipv4[(south <= ipv4['latitude']) & (north >=ipv4['latitude']) & (west <= ipv4['longitude']) & (east >= ipv4['longitude'])]
    # dataa = ipv4[(lat_max <= ipv4['latitude']) & (ipv4['latitude'] <= lat_min)] & (ipv4['longitude'] >= long_max)

    # print('hmm', dataa)

    return dataa.compute().to_json(orient='records')

@app.route('/data', methods=['GET'])
@cross_origin()
def get():
    return json

if __name__ == '__main__':
    app.run(debug=True)