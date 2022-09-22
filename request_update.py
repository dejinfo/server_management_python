from flask import Flask, request, jsonify, make_response
from flask_cors import CORS,cross_origin
import requests                                   #importing the packages/modules
import psycopg2
import INSERT   #inserting the database file
from datetime import date
import data as data
import regex     #it is used to show all the matched characters which are related to the searched one
from connect2DB import *

date_today = date.today()

app = Flask(__name__)
CORS(app)

# @app.route('/request_update', methods=['PUT'])
# def request_update():
#     conn = connectDB()
#     # conn = psycopg2.connect(host='localhost', dbname='server111', user='postgres', password='root',
#     #                         # connection with database naming conn
#     #                         port=5433)
#     cursor = conn.cursor()  # cursor object is created
#     cur = conn.cursor()
#     conn.autocommit = True


@app.route('/request_update', methods=['PUT'])
def UpdateRequest():  # created a function for deleting user with their corresponding

    _json = request.json  # converting the request to json
    ID = _json['ID']
    print(ID, "ID")


    conn = connectDB()
    # Infraadmin_Comments   =  _json["Infraadmin_Comments"]
    Infraadmin_Comments = _json["Infraadmin_Comments"]
    Request= _json["Request"]

    cursor = conn.cursor()

    data = ( ID, Infraadmin_Comments,Request)
    cursor.execute("SELECT * FROM server_request  WHERE ID=%s", (ID,))
    print(data)

    cursor.execute("UPDATE  server_request SET Request= %s WHERE ID =%s",
                   (Request, ID))  # qurey for deleting and it will
    print("kkkkkkk")

    cursor.execute("UPDATE server_request SET Infraadmin_Comments = array_prepend( %s, Infraadmin_Comments) WHERE ID=%s",
                   (Infraadmin_Comments, ID))

    conn.commit()
    cursor.execute('select * from server_request where ID = %s', (ID,))
    data = cursor.fetchall()
    print("data")
    resp = jsonify({'message': 'Server Request updated successfully !!', 'status': '200 OK'})

    resp = jsonify({"message": "updated successfully!", "status": "200 OK"})

    # resp = jsonify('User deleted successfully!')  # response is jsonifying
    resp.status_code = 200  # giving status code as 200 (true)
    return resp


if __name__ == '__main__':
    # app.app_context()
    app.run(host="0.0.0.0",port=5000,debug=True)