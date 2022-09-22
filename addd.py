from urllib import request
from flask_cors import CORS,cross_origin
import psycopg2
# from addserverFORM import app
from flask import Flask, request, jsonify, make_response
import requests                                   #importing the packages/modules
import psycopg2
import INSERT   #inserting the database file
from datetime import date
import data as data
import regex     #it is used to show all the matched characters which are related to the searched one
from connect2DB import *
import socket

date_today = date.today()
import datetime as datetime    #import datetime package

date_today = date.today()
date_time = datetime.datetime.now()

d = datetime.datetime.strptime('2011-06-09', '%Y-%m-%d')    # the time format
my_datetime_utc = date_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')          # here i m using this format

app = Flask(__name__)
CORS(app)

conn = connectDB()  # called the connectDB file to connect with the database
# connecting with the database
# dbase = psycopg2.connect(         #the database is assigned by dbase
#     host='localhost',
#     dbname='server111',
#     user='postgres',
#     password='root',
#     port=5433)
conn.autocommit = True  # if you commit a database, it saves all the changes till that particular point


@cross_origin()
                       #1 # adding_asset  #
@app.route('/add_asset', methods=['POST'])

def add_asset():

    try:

        if request.method == 'POST':  # using POST method to request the data
            cursor = conn.cursor()
            cursor.execute("select Asset_Id from Asset")  # [(1,),(2,)]
            res1 = cursor.fetchall()            #  fetching the data from database
            Id_alr = len(res1)                 # variable id_alr used for the length of the fetched data
            Asset_Id = Id_alr + 1           # here it is incred with +1
            cursor.execute                # it is executed
            _json = request.json            # json format
            print("_json")


            Asset_Name=_json["Asset_Name"]
            Manufacturer = _json["Manufacturer"]
            BMC_IP = _json["BMC_IP"]
            BMC_User= _json["BMC_User"]
            BMC_Password = _json["BMC_Password"]
            Asset_Location = _json["Asset_Location"]
            # Reserved = _json["Reserved"]
            # # assigned_on = _json["assigned_on"]
            # Assigned_to = _json["Assigned_to"]
            # Assigned_from=_json["Assigned_from"]
            # Assigned_by = _json["Assigned_by"]
            Created_on=date_today
            Created_by = _json["Created_by"]
            OS_IP=_json["OS_IP"]
            OS_User=_json["OS_User"]
            OS_Password=_json["OS_Password"]
            # Updated_on=_json["Updated_on"]
            # Updated_by= _json["Updated_by"]
            Purpose = _json["Purpose"]
            Cluster_Id = _json["Cluster_Id"]
            # team_id = _json["team_id"]
            Delete = "0"
            # Status = _json["Status"]
            print("server_id")
            # cursor = conn.cursor()  # created a cursor
            print("zdfrhv")
            regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
            print("reggggg",regex)

            try:
                socket.inet_aton(OS_IP) and socket.inet_aton(BMC_IP)
                query1 = "SELECT Asset_Id FROM Asset"
                print(query1, "q1111")
                cursor.execute(query1)
                fetch = cursor.fetchall()
                print(fetch, "fe1111")
                lst = []
                for i in fetch:
                    for j in i:
                        lst.append(j)
                    print(lst, "lsttt")
                if Asset_Id not in lst:
                    # values to assign in the columns
                    VALUES = (Asset_Id, Asset_Name, Manufacturer, BMC_IP, BMC_User, BMC_Password,
                              Asset_Location,  # Reserved,Assigned_to,Assigned_from,Assigned_by,
                              Created_on, Created_by, OS_IP, OS_User, OS_Password,  # Updated_on,Updated_by,
                              Purpose, Cluster_Id, Delete)  # Delete,Status)
                    print("iohvd")
                    cursor.execute(
                        'INSERT INTO Asset(Asset_Id,Asset_Name,Manufacturer,BMC_ip,BMC_User,'
                        'BMC_Password,Asset_Location,Created_on,Created_by,OS_IP,OS_User,OS_Password,Purpose,Cluster_Id,delete) '
                        'values (%s,%s, %s ,%s ,%s ,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', VALUES)
                    # execute the values using cursor in the server_table to store all the new data
                    print("awxfyn")
                    conn.commit()
                    # conn.commit()  # commit
                    print("oook")
                    cursor.execute('select * from asset')  # to show the data in the asset_table
                    print("fjrdgchk")
                    data = cursor.fetchall()  # it will fetch all the data with variable data

                    print("_id")


                    resp = jsonify(
                       '"Status Code": "200 OK", "Message": "Recorded sucessfully"')  # created a response and jsonifed it
                    resp.status_code = 200  # given a status code 200(truse) to the above response
                    return resp  # returning the response if the above condition works
                print("oooooooooooooooooooooooo")
            except socket.error:
                print("errrrrrrrrrrrrrrrrrrrrrr")
                resp = jsonify('Invalid syntax! ,status code:400 ok')  # created a response and jsonifed it
                return resp

            # query1 ="SELECT Asset_Id FROM Asset"
            # print(query1,"q1111")
            # cursor.execute(query1)
            # fetch = cursor.fetchall()
            # print(fetch,"fe1111")
            # lst = []
            # for i in fetch:
            #     for j in i:
            #         lst.append(j)
            #     print(lst,"lsttt")
            # if Asset_Id not in  lst:
            #
            #         # values to assign in the columns
            #     VALUES = (Asset_Id,Asset_Name,Manufacturer,BMC_IP,BMC_User,BMC_Password,
            #               Asset_Location,#Reserved,Assigned_to,Assigned_from,Assigned_by,
            #               Created_on,Created_by,OS_IP,OS_User,OS_Password,#Updated_on,Updated_by,
            #               Purpose,Cluster_Id,Delete) #Delete,Status)
            #     print("iohvd")
            #     cursor.execute(
            #         'INSERT INTO Asset(Asset_Id,Asset_Name,Manufacturer,BMC_ip,BMC_User,'
            #         'BMC_Password,Asset_Location,Created_on,Created_by,OS_IP,OS_User,OS_Password,Purpose,Cluster_Id,delete) '
            #         'values (%s,%s, %s ,%s ,%s ,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',VALUES)
            #         # execute the values using cursor in the server_table to store all the new data
            #     print("awxfyn")
            #     conn.commit()
            #     # conn.commit()  # commit
            #     print("oook")
            #     cursor.execute('select * from asset') # to show the data in the asset_table
            #     print("fjrdgchk")
            #     data = cursor.fetchall()              #it will fetch all the data with variable data
            #
            #     print("_id")
            #
            #     # serverList = []          #using the for loop to execute all data oneby one and then stored in the serverlist
            #     # for serverData in data:
            #     #     data = {"Asset_ID": serverData[0], "Manufacturer": serverData[1],"BMC_ip": serverData[2], "BMC_User": serverData[3],
            #     #             "BMC_password": serverData[4], "Asset_location": serverData[5],
            #     #             "Reserved": serverData[6],"Assigned_to":serverData[9],"Assigned_from":serverData[8],"Assigned_by":serverData[7],
            #     #             "Created_on":serverData[10],"Created_by":serverData[11],"Updated_on":serverData[12],"Updated_by":serverData[13],"Purpose":serverData[14],"Cluster_Id":serverData[15] ,
            #     #             "Delete":serverData[16],"Status":serverData[17]}
            #
            #
            #         # serverList.append(data)
            #     # return jsonify(serverList)            #it will show list of server with this newly added
            #     resp = jsonify('message:recorded successfully ,status code:200 ok')  # created a response and jsonifed it
            #     resp.status_code = 200  # given a status code 200(truse) to the above response
            #     return resp  # returning the response if the above condition works
    except Exception as exp:
            resp = jsonify('"Message": "Invalid input syntax for IP ", "Status Code": "202"')  # created a response and jsonifed it
            return resp               #return the response
    finally:
        cursor.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)


# regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
#
#
# # Define a function for
# # validate an Ip address
# def check(Ip):
#     # pass the regular expression
#     # and the string in search() method
#     if (re.search(regex, Ip)):
#         print("Valid Ip address")
#
#     else:
#         print("Invalid Ip address")
#

# # Driver Code
# if __name__ == '__main__':
#     # Enter the Ip address
#     Ip = "192.168.0.1"
#
#     # calling run function
#     check(Ip)
#
#     Ip = "110.234.52.124"
#     check(Ip)
#
#     Ip = "366.1.2.2"
#     check(Ip)