
from server_file1 import *
import unittest
import pytest

import pytest
import requests
import json


def test_add_asset():
    url = "http://127.0.0.1:5000/add_asset"

    payload = json.dumps({
        "Asset_Name": "rrrrr",
        "Manufacturer": "api",
        "BMC_IP": "12.3.1.22",
        "BMC_User": "abcd",
        "BMC_password": "abcd123",
        "Asset_location": "mumbai",
        "Created_by": "user",
        "OS_IP": "1.9.0.0",
        "OS_User": "4",
        "OS_Password": "dstcfb",
        "Purpose": "testing",
        "Cluster_Id": "C1"

    })
    headers = {
        'Content-Type': 'application/json'
    }


    response = requests.request("POST", url, headers=headers, data=payload)
    return response

    print("respose", str(response.text))
    assert response.status_code == 200
    expected_data = {
        "message": "Asset updated successfully !!",
        "status": "200 OK"
    }

    assert json.loads(response.text) == expected_data
    expected_message = "Asset updated successfully !!"
    actual_message = json.loads(response.text)["message"]
    assert expected_message == actual_message


# test_add_asset()
test_add_asset()

