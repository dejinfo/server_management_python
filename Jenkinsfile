#api to update asset/servers

from sre_constants import SUCCESS
from ssl import Purpose
from urllib import response
from flask import Flask, request, jsonify
from connect2db import *
import requests

app = Flask(__name__)

@app.route('/update_asset_details' ,methods=['PUT'])
def update_asset_details():
    conn = connectDB()
    if request.method == 'PUT':
            _json = request.json
            asset_id = _json["asset_id"]
            asset_location=  _json["asset_location"]
            purpose = _json["purpose"]
            created_by = _json["created_by"]
            cursor= conn.cursor()
            data = (created_by, asset_location,purpose)
            cursor.execute('select * from asset where asset_id=%s',asset_id)
            sql_update_query = """UPDATE asset set created_by = %s , asset_location = %s , purpose = %s  where asset_id = %s"""
            cursor.execute(sql_update_query, (created_by, asset_location, purpose, asset_id))
            conn.commit()
            cursor.execute('select * from asset where asset_id = %s', asset_id) 
            data = cursor.fetchall()
            resp = jsonify({'message' : 'Asset updated successfully !!', 'status' :'200 OK'})
            print(resp)
            resp.status_code = 200
            v = resp.status_code
            print(v)
            assert v == 200 , "code does'not match"
            return resp
            
        



if __name__ == '__main__':
    # app.app_context()
    app.run(host="0.0.0.0",port=5000,debug=True)