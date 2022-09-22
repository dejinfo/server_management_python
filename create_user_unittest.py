import json

from unittest import TestCase
from unittest.mock import patch

import requests


# class TestAnalytics(TestCase):
#
#     @patch('requests.post')
#     def test_post(self, mock_post):
#         info = {"User_ID": 16,
#     "Email_ID": "six@gmail.com",
#     "Password": "password@123",
#     "First_Name": "sus",
#     "Last_Name": "K ",
#     "Created_by":"Sreedhar",
#     "Updated_by":"ramana",
#     "Role":"infra-admin",
#     "Teams": "T6",
#     "Delete": "1"}
#         resp = requests.post("http://127.0.0.1:5000/create_user", data=json.dumps(info), headers={'Content-Type': 'application/json'})
#         print(resp,"resppp")
#         # mock_post.assert_called_with("http://127.0.0.1:5000/create_user", data=json.dumps(info), headers={'Content-Type': 'application/json'})
#
#         # resp = requests.get(url)
#         # print(resp, "repp")
#         Data = resp.content
#         print(Data, "DATAAA")
#         # assert (resp.status_code == 200)
#         self.assertEqual(resp, Data)
#         return Data
#
#
# TestAnalytics().test_post()


import json
import unittest
from app import app
# set our application to testing mode
app.testing = True
class TestApi (unittest.TestCase):
    def test_main (self):
        with app.test_client () as client:
         sent = {"User_ID": 16,
    "Email_ID": "six@gmail.com",
    "Password": "password@123",
    "First_Name": "sus",
    "Last_Name": "K ",
    "Created_by":"Sreedhar",
    "Updated_by":"ramana",
    "Role":"infra-admin",
    "Teams": "T6",
    "Delete": "1"}
         print(sent, "senttt")

         result = client.post('http://127.0.0.1:5000/create_user', data=sent) # check result from server with expected data
         print(result,"resultt")
         self.assertEqual (result.data, json.dumps(sent))
