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
            query1 ="SELECT Asset_Id FROM Asset"
            print(query1,"q1111")
            cursor.execute(query1)
            fetch = cursor.fetchall()
            print(fetch,"fe1111")
            lst = []
            for i in fetch:
                for j in i:
                    lst.append(j)
                print(lst,"lsttt")
            if Asset_Id not in  lst:

                    # values to assign in the columns
                VALUES = (Asset_Id,Asset_Name,Manufacturer,BMC_IP,BMC_User,BMC_Password,
                          Asset_Location,#Reserved,Assigned_to,Assigned_from,Assigned_by,
                          Created_on,Created_by,OS_IP,OS_User,OS_Password,#Updated_on,Updated_by,
                          Purpose,Cluster_Id,Delete) #Delete,Status)
                print("iohvd")
                cursor.execute(
                    'INSERT INTO Asset(Asset_Id,Asset_Name,Manufacturer,BMC_ip,BMC_User,'
                    'BMC_Password,Asset_Location,Created_on,Created_by,OS_IP,OS_User,OS_Password,Purpose,Cluster_Id,delete) '
                    'values (%s,%s, %s ,%s ,%s ,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',VALUES)
                    # execute the values using cursor in the server_table to store all the new data
                print("awxfyn")
                conn.commit()
                # conn.commit()  # commit
                print("oook")
                cursor.execute('select * from asset') # to show the data in the asset_table
                print("fjrdgchk")
                data = cursor.fetchall()              #it will fetch all the data with variable data

                print("_id")

                # serverList = []          #using the for loop to execute all data oneby one and then stored in the serverlist
                # for serverData in data:
                #     data = {"Asset_ID": serverData[0], "Manufacturer": serverData[1],"BMC_ip": serverData[2], "BMC_User": serverData[3],
                #             "BMC_password": serverData[4], "Asset_location": serverData[5],
                #             "Reserved": serverData[6],"Assigned_to":serverData[9],"Assigned_from":serverData[8],"Assigned_by":serverData[7],
                #             "Created_on":serverData[10],"Created_by":serverData[11],"Updated_on":serverData[12],"Updated_by":serverData[13],"Purpose":serverData[14],"Cluster_Id":serverData[15] ,
                #             "Delete":serverData[16],"Status":serverData[17]}


                    # serverList.append(data)
                # return jsonify(serverList)            #it will show list of server with this newly added
                resp = jsonify('message:recorded successfully ,status code:200 ok')  # created a response and jsonifed it
                resp.status_code = 200  # given a status code 200(truse) to the above response
                return resp  # returning the response if the above condition works
    except Exception as exp:
            resp = jsonify('message:AlreadyExist ,status code:400 ok')  # created a response and jsonifed it
            return resp               #return the response
    finally:
        cursor.close()

                   # 2   #list_asset#

@app.route('/list_asset', methods=["GET"])
def view_server():
    # conn = connectDB()
    try:
        print(conn,"kkkkkk")

        cursor = conn.cursor()
        # conn.autocommit = True

        if request.method == 'GET':  # GET method is used here
            cursor.execute("select * from asset WHERE delete =B'0'")  # store inserver_table

            data = cursor.fetchall()  # crusor fetchs all the data
            serverl = []  # serverlist for get method with variable serverl
            for serverData in data:


                jsonData =  {"Asset_ID": serverData[0],"Asset_Name":serverData[1],"Manufacturer": serverData[2],"BMC_IP": serverData[3], "BMC_User": serverData[4],
                        # "BMC_password": serverData[4],
                        "Asset_Location": serverData[6],"Reserved": serverData[7],"OS_IP":serverData[15],"Assigned_to": serverData[8],"Assigned_from":serverData[9],"Assigned_by": serverData[10],
            "OS_User":serverData[16],
                        "Created_on":serverData[11],"Created_by":serverData[12],"Updated_on":serverData[13],"Updated_by":serverData[14],
                             "Purpose":serverData[18],"Cluster_Id":serverData[19] ,
                         "Delete":serverData[20],
                    "Status":serverData[21]}
                serverl.append(jsonData)  # it will show all the data stored in the database with key:value
        a = []
        for i in serverl:

            cursor.execute("select email_id from users where user_id=%s", [i['Assigned_to']])              # select the email id from user table a it is sameas assigned to
            res = cursor.fetchall()                                # it will fetch all the data
            print(res)
            for j in res:
                i.update({"Assigned_to": j[0].split("@")[0]})              #it will split the email id and print the first name only
            a.append(i)
        datavar = []
        for i in serverl:
            if i["Created_on"]:
                created_date = i["Created_on"]                         #here changing the format to "2022-10-03T00:00:00Z"
                date_time_obj = created_date.isoformat() + 'Z'
                i.update({"Created_on": date_time_obj})
            if i["Updated_on"]:
                Updated_date = i["Updated_on"]
                date_time_obj1 = Updated_date.isoformat() + 'Z'
                i.update({"Updated_on": date_time_obj1})
            if i["Assigned_from"]:
                Updated_date = i["Assigned_from"]
                date_time_obj1 = Updated_date.isoformat() + 'Z'
                i.update({"Assigned_from": date_time_obj1})
            datavar.append(i)
            # print("datauserrr", datavar)
        return jsonify({"message":"listing all assets","status code": '200 OK',"ListAsset":datavar})           # response message
    except Exception as e:
        print(e)
    finally:
        cursor.close()

# 3 # delete_asset#

@app.route('/delete_asset', methods=['PUT'])
def delete_ser():  # created a function for deleting user with their corresponding
    try:

        _json = request.json  # converting the request to json
        Asset_Id = _json['Asset_Id']
        print(Asset_Id, "Asset_Id")

        conn = connectDB()  # connecting to the database
        cursor = conn.cursor()  # created a cursor function and giving cursor_factory=RealDictCursor
        curs = conn.cursor()
        cursor.execute("SELECT * FROM asset  WHERE Asset_Id=%s",
                       (Asset_Id,))  # qurey for selecting the datas with the given id
        # and given to the cursor and it will execute
        db22 = cursor.fetchall()  # fetching all the datas of that corresponding id
        print(db22, "db22")

        if len(db22) != 0:  # checking condition if the user is not null
            cursor.execute("UPDATE  asset SET DELETE ='1',Reserved= False,Updated_on=%s WHERE Asset_Id =%s", [date.today() ,(Asset_Id,)])  # qurey for deleting and it will
            # work only the value is not equal to null
            curs.execute(
                "SELECT Asset_Id,Assigned_to,Assigned_from,Updated_on,Updated_by FROM ASSET WHERE Asset_Id =%s",
            (Asset_Id,))
            print("axydt cgbi; kn/on'i")
            data = curs.fetchall()  # fetching all the datas of that corresponding id
            print(data, "dattttaa")
            remarks = "remark"

            lst = []
            for i in data:
                for j in i:
                    lst.append(j)
                    # lst.append()
            print(lst, "lsssttttt")  # it will print the list lst
            print(lst[0], "ppppp")
            # print(lst[1],"qqqq")
            # print(lst[2],"ooo")
            # print(lst[3],"333")
            # print(lst[4],"44")
            lst2 = lst + [remarks]  # creating another list to add the string format REMARK with that list lst
            print(lst2, "l222")

            query = (lst2[0], lst2[1], lst2[2], lst2[3], lst2[4],
                     lst2[5])  # query to get all the fields starting from index 0 to 5
            # print(query,"qqq")
            # print(lst[0],"1lst")
            # print(lst[0],"9999")
            curs.execute(
                'INSERT INTO  historic_details(Asset_Id,Assigned_to,Assigned_from,Updated_on,Updated_by,remarks)values (%s, %s ,%s ,%s ,%s,%s)',
                query)  # insert query

            print(query, "queryyyyyyyyy")  # it will print the query



            conn.commit()
            resp = jsonify({"message": "asset deleted successfully!", "status": "200 OK"})

            # resp = jsonify('User deleted successfully!')  # response is jsonifying
            resp.status_code = 200  # giving status code as 200 (true)
            return resp  # if the above condition works thengive the response as 200



        else:
            resp = jsonify({"message": "ASSET_ID IS NOT THERE!", "status": "400 Bad Request"})
            # res = jsonify("User not available with  id ", User_Id)  # if the user is null then this response works
            resp.status_code = 400  # error response
            return resp

    except Exception as e:
        print(e)
    finally:
        cursor.close()

  #if assigned from is null ,then it will show error like violates not null constraint
  #in postman it is showing like this -
#   The view function for 'delete_ser' did not return a valid response. The function either returned None or ended without a return statement


      #4 #platform_profile#

@app.route('/platformProfile', methods=['GET'])
def getfile():
        print("vgsduofwedj")


        with open("platformprofile.json", "r+") as f:
            data = f.read()
        return data

   #5 #update the request_form#

@app.route('/request_update', methods=['PUT'])
def UpdateRequest():  # created a function for deleting user with their corresponding

    conn = connectDB()
    if request.method == 'PUT':
        _json = request.json                #the put method withjson format
        ID = _json["ID"]

        # Infraadmin_Comments   =  _json["Infraadmin_Comments"]
        Infraadmin_Comments = _json["Infraadmin_Comments"]
        Request= _json["Request"]

        cursor = conn.cursor()            # cursor used

        data = ( ID, Infraadmin_Comments,Request)      #value
        cursor.execute("SELECT * FROM server_request  WHERE ID=%s", (ID,))       # execute query with id
        print(data)

        cursor.execute("UPDATE  server_request SET Request= %s WHERE ID =%s",
                       (Request, ID))  # qurey for updating the request column using id
        print("kkkkkkk")

        cursor.execute(
            "UPDATE server_request SET Infraadmin_Comments = array_prepend( %s, Infraadmin_Comments) WHERE ID=%s",
            [str(Infraadmin_Comments) + str(my_datetime_utc), ID])                # updating thecomment section with today date and time
        conn.commit()           #commit
        cursor.execute('select * from server_request where ID = %s', (ID,))
        data = cursor.fetchall()         # it fetches all the data
        print("data")


        resp = jsonify({"message": "updated successfully!", "status": "200 OK"})      # final message it will print

        # resp = jsonify('User deleted successfully!')  # response is jsonifying
        resp.status_code = 200  # giving status code as 200 (true)
        return resp



if __name__ == '__main__':
    # app.app_context()
    app.run(host="0.0.0.0",port=5000,debug=True)