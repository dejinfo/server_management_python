from user_api import convert_json


def test_myasset(self):
    cursor = base.cursor()
    Assigned_to = 5
    cursor.execute(
        "select asset_id,manufacturer,bmc_ip,bmc_user,asset_location,reserved,assigned_to,assigned_from,assigned_by,created_on,created_by,updated_on,updated_by,os_ip,os_user,purpose,cluster_id,delete,status from asset where Assigned_to=%s",
        [Assigned_to])
    arr = ["Asset_ID", "Manufacturer", "BMC_IP", "BMC_USER", "Asset_location", "Reserved", "Assigned_to",
           "Assigned_from", "Assigned_by", "Created_on", "Created_by", "Updated_on", "Updated_by", "OS_IP",
           "OS_User", "Purpose", "Cluster_Id", "Delete", "Status"]
    resulttt = cursor.fetchall()
    json_data = convert_json(resulttt, arr)

    data = []
    a = []
    for i in json_data:
        cursor.execute("select email_id from users where user_id=%s", [i['Assigned_to']])
        res = cursor.fetchall()
        print(res)
        for j in res:
            i.update({"Assigned_to": j[0].split("@")[0]})
        if i["Assigned_from"]:
            actual_date = i["Assigned_from"]
            date_time_obj = actual_date.isoformat() + 'Z'
            i.update({"Assigned_from": date_time_obj})
        if i["Updated_on"]:
            actual_date = i["Updated_on"]
            date_time_obj1 = actual_date.isoformat() + 'Z'
            i.update({"Updated_on": date_time_obj1})
        if i["Created_on"]:
            actual_date = i["Created_on"]
            date_time_obj1 = actual_date.isoformat() + 'Z'
            i.update({"Created_on": date_time_obj1})
        data.append(i)

    for i in data:
        sortedDict = dict(sorted(i.items(), key=lambda x: x[0].lower()))
        a.append(sortedDict)
    url = "http://127.0.0.1:5000/my_asset"
    response = requests.post(url=url, json={"Assigned_to": 5})
    e = response.content  # Display response content
    f = e.decode()
    j = json.loads(f)
    ac = j["ListAsset"]
    self.assertEqual(a, ac)
