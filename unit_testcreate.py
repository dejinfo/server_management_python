from adminapi import *
import unittest
import pytest

import pytest
import requests
import json


def test_add_user():
    url = "http://127.0.0.1:5000/create_user"

    payload = json.dumps({
    "Email_Id": "amal@gmail.com",
    "Password": "password@123",
    "First_Name": "amal",
    "Last_Name": "K ",
    "Created_by":"Sreedhar",
    "Role":"infra-admin",
    "Teams": "T6"
})
    headers = {
        'Content-Type': 'application/json'
    }


    response = requests.request("POST", url, headers=headers, data=payload)
    return response

    print("respose", str(response.text))
    assert response.status_code == 200
    expected_data = {
        "message": "User added successfully!",
        "status": "200 OK"
    }

    assert json.loads(response.text) == expected_data
    expected_message = "User added successfully!"
    actual_message = json.loads(response.text)["message"]
    assert expected_message == actual_message


# test_add_asset()
test_add_user()

