import json

from flask_cors import CORS,cross_origin
import psycopg2
import unittest
from flask import Flask, request, jsonify, make_response
import requests  #importing the packages/modules
from connect2DB import *

app = Flask(__name__)
CORS(app)

conn = connectDB()                  #calling the function to connect with the database
conn.autocommit = True
from connect2DB import *
class Testing(unittest.TestCase):
    def test_list_users(self):
        tester = app.test_client(self)
        cursor1 = conn.cursor()
        cursor1.execute("select * from Users ")
        a = cursor1.fetchall()
        user = []  # serverlist for get method with variable serverl
        for userdata in a:
            jsonData = {"User_ID": userdata[0], "Email_ID": userdata[1], "Password": userdata[2],
                        "First_Name": userdata[3], "Last_Name": userdata[4], "Created_on": userdata[5],
                        "Created_by": userdata[6], "Updated_on": userdata[7], "Updated_by": userdata[8],
                        "Role": userdata[9], "Teams": userdata[10], "Delete": userdata[11],
                        }
            user.append(jsonData)
            print(jsonData)
            return (user)


        url = "http://127.0.0.1:5000/view_users"
        resp = requests.get(url)
        Data = resp.content
        r_decod = Data.decode()
        Data1 = json.loads(r_decod)
        print(Data1)
        self.assertEqual(a, Data1)

# class CreateUser(unittest.TestCase):
#     def create_user(self):
#         cursor1 = conn.cursor()

if __name__ == "__main__":
   unittest.main()

