from flask import Flask
from flask_cors import CORS, cross_origin
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import os
import pandas as pd
import json

app = Flask(__name__)
cors = CORS(app)
dirname = os.path.dirname(__file__)
app.config['CORS_HEADERS'] = 'Content-Type'

zipDataUrl = 'http://geolite.maxmind.com/download/geoip/database/Geolite2-City-CSV.zip'
response = urlopen(zipDataUrl)
zipfile = ZipFile(BytesIO(response.read()))
print(zipfile.namelist())
# csvfile = os.path.join(dirname, 'GeoLite2-City-Blocks-IPv4.csv')
#
# df = pd.read_csv(csvfile, dtype={
#     "network" : str,
#     "geoname_id" : str,
#     "registered_country_geoname_id" : str,
#     "represented_country_geoname_id" : str,
#     "is_anonymous_proxy" : str,
#     "is_satellite_provider" : str,
#     "postal_code" : str,
#     "latitude" : str,
#     "longitude" : str,
#     "accuracy_radius" : str,
# })
# df = df.drop(['network', 'geoname_id', 'accuracy_radius','is_satellite_provider'
# ,'is_anonymous_proxy', 'represented_country_geoname_id',
# 'registered_country_geoname_id', 'postal_code' ], axis=1)
# data = df.to_dict(orient='records')
# json = json.dumps(data)
# # print(df.iloc[1])
print(json[0])
@app.route('/')
@cross_origin()
def hello_world():
    return 'hello world'

@app.route('/data', methods=['GET'])
@cross_origin()
def get():
    return json
