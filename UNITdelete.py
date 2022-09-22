from server_file1 import *
import unittest
import pytest

import pytest
import requests
import json


def test_delete_asset():
    url = "http://127.0.0.1:5000/delete_asset"

    payload = json.dumps({
      " Asset_Id ":1 })
    headers = {   'Content-Type': 'application/json'   }


    response = requests.request("PUT", url, headers=headers, data=payload)
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
test_delete_asset()
