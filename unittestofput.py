from adminapi import *
import unittest
import pytest

import pytest
import requests
import json


def test_update_user():
    url = "http://127.0.0.1:5000/update_users"

    payload = json.dumps({
    "User_Id": 7,
    "First_Name": "anjana",
    "Last_Name": "pm",
    "Updated_by":"ramana sir",
    "Role":"infra-admin",
    "Teams": "T6"
})
    headers = {
        'Content-Type': 'application/json'
    }


    response = requests.request("PUT", url, headers=headers, data=payload)
    return response

    print("respose", str(response.text))
    assert response.status_code == 200
    expected_data = {
        "message": "User updated successfully!",
        "status": "200 OK"
    }

    assert json.loads(response.text) == expected_data
    expected_message = "User updated successfully!"
    actual_message = json.loads(response.text)["message"]
    assert expected_message == actual_message


# test_add_asset()
test_update_user()

