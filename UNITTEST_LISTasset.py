import unittest
from server_file1 import *

class Testing(unittest.TestCase):
    def test_list_asset(self):
        tester = app.test_client(self)
        cursor1 = conn.cursor()
        cursor1.execute("select * from asset ")
        a = cursor1.fetchall()
        serverl = []  # serverlist for get method with variable serverl
        for serverData in a:
            jsonData = {"Asset_ID": serverData[0],"Asset_Name":serverData[1], "Manufacturer": serverData[2], "BMC_ip": serverData[3],
                        "BMC_User": serverData[4],
                        # "BMC_password": serverData[4],
                        "Asset_location": serverData[6], "Reserved": serverData[7], "OS_IP": serverData[15],
                        "Assigned_to": serverData[8], "Assigned_from": serverData[9], "Assigned_by": serverData[10],
                        "OS_User": serverData[11],
                        "Created_on": serverData[12], "Created_by": serverData[13], "Updated_on": serverData[14],
                        "Updated_by": serverData[15],
                        "Purpose": serverData[18], "Cluster_Id": serverData[19],
                        "Delete": serverData[20],
                        "Status": serverData[21]}
            serverl.append(jsonData)
            print(jsonData,"rrtrtttyyt")

            return (serverl)
        print(serverl)


        url = "http://127.0.0.1:5000/list_asset"
        resp = requests.get(url)
        Data = resp.content
        r_decod = Data.decode()
        Data1 = json.loads(r_decod)
        print(Data1)
        self.assertEqual(a, Data1)


if __name__ == "__main__":
   unittest.main()



