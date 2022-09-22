# import pytest
# import requests
# import json
#
# from flask_cors import CORS,cross_origin
# import psycopg2
# import unittest
# from flask import Flask, request, jsonify, make_response
# import requests  #importing the packages/modules
# from connect2DB import *
#
#
# app = Flask(__name__)
#
# import unittest
# import json
# import requests
# from connect2DB import *
# class Testing3(unittest.TestCase):
#     def test_api(self):
#         base = connectDB()
#         base.autocommit = True
#         cur = base.cursor()
#         cur.execute('SELECT * FROM users where User_Id=%s', "4")
#         res = cur.fetchall()
#         l = []
#         for i in res:
#             for j in i:
#                 l.append(j)
#         #print(l[2])
#         stored_password = l[11]
#         url = "http://127.0.0.1:5000/delete_user?User_Id=4"  # api url
#         response = requests.get(url)
#         e = response.content  # Display response content
#         f = e.decode()
#         j = json.loads(f)
#         result=j.get("message")
#         print(result)
#
#         self.assertEqual(stored_password,result)

import unittest
import pytest

import pytest
import requests
import json
from adminapi import *



def test_delete_user():
    url = "http://127.0.0.1:5000/delete_user"

    payload = json.dumps({
            "User_Id": 11
          })
    headers = {
        'Content-Type': 'application/json'
    }


    response = requests.request("PUT", url, headers=headers, data=payload)
    return response

    print("respose", str(response.text))
    assert response.status_code == 200
    expected_data = {
        "message": "User deleted successfully!",
        "status": "200 OK"
    }

    assert json.loads(response.text) == expected_data
    expected_message = "User deleted successfully!",
    actual_message = json.loads(response.text)["message"]
    assert expected_message == actual_message


# test_add_asset()
test_delete_user()

