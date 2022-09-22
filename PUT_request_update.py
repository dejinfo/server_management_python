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
    # id so thats why the id passing as an argument it will call in the url
    # id = int(id)
    # print(id, "id")
    _json = request.json  # converting the request to json
    ID = _json['ID']
    print(ID, "ID")
    Request = _json['Request']
    Infraadmin_Comments=_json['Infraadmin_Comments']
    print(Request, "Request")

    conn = connectDB()  # connecting to the database
    cursor = conn.cursor()  # created a cursor function and giving cursor_factory=RealDictCursor

    cursor.execute("SELECT * FROM server_request  WHERE ID=%s", (ID,))  # qurey for selecting the datas with the given id
    # and given to the cursor and it will execute
    db22 = cursor.fetchall()  # fetching all the datas of that corresponding id
    print(db22, "db22")

    cursor.execute("UPDATE  server_request SET Request= %s,Infraadmin_Comments=%s WHERE ID =%s", (Request,Infraadmin_Comments,ID))  # qurey for deleting and it will
    print("kkkkkkk")
        # work only the value is not equal to null
    conn.commit()
    resp = jsonify({"message": "updated successfully!", "status": "200 OK"})

        # resp = jsonify('User deleted successfully!')  # response is jsonifying
    resp.status_code = 200  # giving status code as 200 (true)
    return resp  # if the above condition works thengive the response as 200
    # else:
    #     resp = jsonify({"message": "User doesn't exists!","status": "400 Bad Request"})
    #     # res = jsonify("User not available with  id ", User_ID)  # if the user is null then this response works
    #     resp.status_code = 400  # error response
    #     return resp


if __name__ == '__main__':
    # app.app_context()
    app.run(host="0.0.0.0",port=5000,debug=True)