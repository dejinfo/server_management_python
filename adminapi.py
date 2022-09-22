import datetime as datetime
from datetime import date

from flask import Flask, request
from flask import jsonify
from flask_cors import CORS, cross_origin
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash

from connect2DB import *

date_today = date.today()
date_time = datetime.datetime.now()
d = datetime.datetime.strptime('2011-06-09', '%Y-%m-%d')
my_datetime_utc = date_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')

app = Flask(__name__)
CORS(app)


def convert_json(l_o_t, key):
    b = []
    # iterating  the list of tuples to get individual tuples.
    for item in l_o_t:
        a = {}
        # taking range from 0 to number of items in tuples - 1
        for i in range(len(item)):
            a[key[i]] = item[
                i]  # appending value to dictionary by mapping key from array to value in tuples using indexing.
        b.append(a)  # appending all dictionaries to a list.
    return b


""" Creating new users """


@cross_origin()
@app.route('/create_user', methods=['POST'])
def create_User():
    try:

        conn = connectDB()
        cursor = conn.cursor()  # created a cursor
        cursor.execute("select User_Id from Users")  # [(1,),(2,)]
        res1 = cursor.fetchall()
        Id_alr = len(res1)
        User_Id = Id_alr + 1

        _json = request.json  # converting to json
        # User_Id = _json['User_Id']
        # print(User_Id, "User_Id")
        Email_Id = _json['Email_Id']
        print(Email_Id, "Email_Id")
        Password = _json['Password']
        print(Password, "PASSSWORD")
        First_Name = _json['First_Name']
        print(First_Name, "First_Name")
        Last_Name = _json['Last_Name']
        print(Last_Name, "Last_Name")
        Created_on = date_today
        print(Created_on, "Created_on")
        Created_by = _json['Created_by']
        print(Created_by, "Created_by")
        # Updated_on = date_today
        # print(Updated_on, "Updated_on")
        # Updated_by = _json['Updated_by']
        # print(Updated_by, "Updated_by")
        Role = _json['Role']
        print(Role, "Role")
        Teams = _json['Teams']
        print(Teams, "Teams")
        # Delete = _json['Delete']
        Delete = "0"
        # delete = dele.encode()
        print(Delete, "deletee", Delete)

        # validate the received values
        if User_Id and Email_Id and Password and First_Name and Last_Name and \
                Created_on and Created_by and Role and Teams and Delete and request.method == 'POST':  # giving condition whether the method is post
            _hashed_password = generate_password_hash(
                Password)  # using an inbuilt function generate_password_hash the password is hashing
            # save edits

            query1 = ("SELECT User_Id FROM Users ")  # qurey for selecting userid id from the usertable
            print(query1, "q1111")
            cursor.execute(query1)  # executing the qurey
            db224 = cursor.fetchall()  # fetching the qurey
            print(db224, "db224")
            usrid = []  # created an empty list for adding the user ids
            for i in db224:  # iterating the fetched values
                for j in i:  # iterating the tuples
                    print(usrid, "useridd")
                    usrid.append(j)  # appending the values in to the list
                print(usrid, "idddddd")

            if User_Id in usrid:  # checking the user id is present in the list
                resp = jsonify({"Message": "Userid is already exists!",
                                "Status": "400 Bad Request"})  # if the userid is present in the list it will show response as this
                resp.status_code = 400  # status code made as 400
                return resp  # this response will work if this condition works

            query = ("SELECT Email_Id FROM Users ")  # qurey for selecting email id from the usertable
            cursor.execute(query)  # executing the qurey
            db223 = cursor.fetchall()  # fetching the qurey
            emailid = []  # created an empty list for adding the email ids

            for i in db223:  # iterating the fetched values
                for j in i:  # iterating the tuples
                    emailid.append(j)  # appending the values in to the list

            if Email_Id in emailid:  # checking the email id is present in the list
                resp = jsonify({"Message": "Email is already exists!", "Status": "400 Bad Request"})
                # resp = jsonify(
                #     'Email is already exists!')  # if the emailid is present in the list it will show response as this
                resp.status_code = 400  # status code made as 400
                return resp  # this response will work if this condition works

            else:
                sql = "INSERT INTO Users(User_Id, Email_Id, Password,First_Name ,Last_Name , Created_on , created_by ,Role,Teams,delete)" \
                      " VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"  # qurey for inserting values to the sql
                print(sql, "sqlll")
                data = (User_Id, Email_Id, _hashed_password, First_Name, Last_Name, Created_on, Created_by,
                        Role, Teams, Delete)  # passing the variables from frondend to data
                print(data, "dataa")
                # connecting to psql

                cursor.execute(sql, data)  # executed the cursor with the sql qurey and the datas inserting
                conn.commit()  # commited the conn
                resp = jsonify(
                    {"Message": "User added successfully!", "Status": "200 OK"})  # created a response and jsonifed it
                # resp.status_code = 200  # given a status code 200(truse) to the above response
                return resp  # returning the response if the above condition works

        else:
            res = jsonify({"Message":"User is not added please check the error below!","Status":"404 NOT FOUND"})  # created a response and jsonifed it
            res.status_code = 404  # giving error status
            return res
    except Exception as e:
        print(e)
    finally:
        cursor.close()


@app.route('/view_users', methods=["GET"])
def list_users():
    try:
        conn = connectDB()
        print(conn, "kkkkkk")
        cursor = conn.cursor()
        conn.autocommit = True

        if request.method == 'GET':  # GET method is used here
            cursor.execute("select * from Users where delete =B'0'")  # store inserver_table
            data = cursor.fetchall()  # crusor fetchs all the data
            user = []  # serverlist for get method with variable serverl
            for userdata in data:
                jsonData = {"User_Id": userdata[0], "Email_Id": userdata[1], "Password": userdata[2],
                            "First_Name": userdata[3], "Last_Name": userdata[4], "Created_on": userdata[5],
                            "Created_by": userdata[6], "Updated_on": userdata[7], "Updated_by": userdata[8],
                            "Role": userdata[9], "Teams": userdata[10], "Delete": userdata[11],
                            }
                user.append(jsonData)  # it will show all the data stored in the database with key:value
            data_user = []
            for i in user:
                if i["Created_on"]:
                    created_date = i["Created_on"]
                    date_time_obj = created_date.isoformat() + 'Z'
                    i.update({"Created_on": date_time_obj})
                if i["Updated_on"]:
                    Updated_date = i["Updated_on"]
                    date_time_obj1 = Updated_date.isoformat() + 'Z'
                    i.update({"Updated_on": date_time_obj1})
                data_user.append(i)
                print("datauserrr", data_user)

        return jsonify({"Message": "Record found", "Status code": '200 OK', "Listusers": data_user[::-1]})

    except Exception as e:
        print(e)
    finally:
        cursor.close()


@app.route('/update_users', methods=['PUT'])
def update_User():
    try:

        _json = request.json  # converting the request to json
        User_Id = _json['User_Id']
        print(User_Id, "User_Id")
        # Email_Id = _json['Email_Id']
        # print(Email_Id, "Email_Id")
        # Password = _json['Password']
        # print(Password, "PASSSWORD")
        First_Name = _json['First_Name']
        print(First_Name, "First_Name")
        Last_Name = _json['Last_Name']
        print(Last_Name, "Last_Name")
        # Created_on = date_today
        # print(Created_on, "Created_on")
        # Created_by = _json['Created_by']
        # print(Created_by, "Created_by")
        Updated_on = date_today
        print(Updated_on, "Updated_on")
        Updated_by = _json['Updated_by']
        print(Updated_by, "Updated_by")
        Role = _json['Role']
        print(Role, "Role")
        Teams = _json['Teams']
        print(Teams, "Teams")
        # Delete = _json['Delete']
        # delete = dele.encode()
        # print(Delete, "deletee", Delete)

        # validate the received values
        if User_Id and First_Name and Last_Name and \
                Updated_on and Updated_by and Role and Teams and request.method == 'PUT':
            # _hashed_password = generate_password_hash(Password)  # do not save password as a plain text so the
            # generate_password_hash will encrypt the password
            # save edits
            sql = "UPDATE Users SET First_Name = %s," \
                  " Last_Name = %s, Updated_on = %s,Updated_by=%s, Role=%s, Teams=%s WHERE User_Id=%s "  # qurey for updating
            print(sql, "sqlllllll")
            data = (First_Name, Last_Name, Updated_on, Updated_by, Role, Teams,
                    User_Id
                    )  # taking the datas from frondend and passing in to a variable
            print(data, "dataaa")
            conn = connectDB()  # connecting to the database
            cursor = conn.cursor()
            query1 = "SELECT User_Id FROM Users"  # qurey for selecting email id from the usertable
            print(query1, "qq11")
            cursor.execute(query1)  # executing the qurey
            db223 = cursor.fetchall()  # fetching the qurey
            print(db223, "db22")
            userid = []  # created an empty list for adding the email ids

            for i in db223:  # iterating the fetched values
                for j in i:  # iterating the tuples
                    userid.append(j)
            print(userid, "userrr")
            if User_Id in userid:
                cursor.execute(sql, data)  # executing the qurey and the datas from frond end
                conn.commit()
                resp = jsonify({"Message": "User updated successfully!", "Status": "200 OK"})
                # resp = jsonify('User updated successfully!')  # jsonifying the response
                resp.status_code = 200  # making the status as 200 (true)
                conn.close()
                return resp  # if the above condition works then giving the response 200
            else:
                resp = jsonify({"Message": "User doesn't exists!", "Status": "400 Bad Request"})
                # resp = jsonify('no userid!')  # if the userid is present in the list it will show response as this
                resp.status_code = 400  # status code made as 400
                return resp
        else:
            resp = jsonify({"Message": "Please check the error below!", "Status": "400 Bad Request"})
            # res = jsonify('User not found')  # jsonifying the response
            resp.status_code = 400  # giving status code 400 (False)
            return resp  # returning the response

    except Exception as e:
        print(e)
    finally:
        cursor.close()


@app.route('/delete_user', methods=['PUT'])
def delete_user():  # created a function for deleting user with their corresponding
    try:
        # id so thats why the id passing as an argument it will call in the url
        # id = int(id)
        # print(id, "id")
        _json = request.json  # converting the request to json
        User_Id = _json['User_Id']
        print(User_Id, "User_Id")

        conn = connectDB()  # connecting to the database
        cursor = conn.cursor()  # created a cursor function and giving cursor_factory=RealDictCursor

        cursor.execute("SELECT * FROM Users  WHERE User_Id=%s",
                       (User_Id,))  # qurey for selecting the datas with the given id
        # and given to the cursor and it will execute
        db22 = cursor.fetchall()  # fetching all the datas of that corresponding id
        print(db22, "db22")
        """test"""
        query1 = "SELECT User_Id FROM Users WHERE DELETE ='1' ;"
        print(query1, "qqq1111")
        cursor.execute(query1)
        db33 = cursor.fetchall()
        print(db33, "db3333333333")
        dele = []
        for i in db33:
            # print(i,"iii")
            for j in i:
                # print(j,"jjjj")
                dele.append(j)
        print(dele, "dele")
        if User_Id in dele:
            print("its already deleted")
            resp = jsonify({"Message": "This is already deleted!", "Status": "400 Bad Request"})
            # res = jsonify('This is already deleted!')  # jsonifying the response
            resp.status_code = 400  # giving status code 400 (False)
            return resp

        """endtest"""
        if len(db22) != 0:  # checking condition if the user is not null
            cursor.execute("UPDATE  Users SET DELETE ='1'WHERE User_Id =%s",
                           (User_Id,))  # qurey for deleting and it will
            # work only the value is not equal to null
            conn.commit()
            resp = jsonify({"Message": "User deleted successfully!", "Status": "200 OK"})

            # resp = jsonify('User deleted successfully!')  # response is jsonifying
            resp.status_code = 200  # giving status code as 200 (true)
            return resp  # if the above condition works thengive the response as 200
        else:
            resp = jsonify({"Message": "User doesn't exists!", "Status": "400 Bad Request"})
            # res = jsonify("User not available with  id ", User_Id)  # if the user is null then this response works
            resp.Status_code = 400  # error response
            return resp

    except Exception as e:
        print(e)
    finally:
        cursor.close()


@app.route('/create_request', methods=['POST'])
def create_request():
    try:
        conn = connectDB()
        cursor = conn.cursor()  # created a cursor
        print(cursor, "cursoor")

        cursor.execute("select Id from Server_Request")  # [(1,),(2,)]
        res1 = cursor.fetchall()
        Id_alr = len(res1)
        Id = Id_alr + 1

        _json = request.json  # converting to json
        # Id = _json['Id']
        # print(Id, "Id")
        User_No = _json['User_No']
        print(User_No,"User_No")
        Creator = _json['Creator']
        print(Creator, "Creator")
        Start_Date = _json['Start_Date']
        print(Start_Date, "Start_Date")
        End_Date = _json['End_Date']
        print(End_Date, "End_Date")
        Manufacturer = _json['Manufacturer']
        print(Manufacturer, "Manufacturer")
        # Created_on = date_today
        # print(Created_on, "Created_on")
        Number_Of_Servers = _json['Number_Of_Servers']
        print(Number_Of_Servers, "Number_Of_Servers")
        Operating_System = _json['Operating_System']
        print(Operating_System,"Operating_System")
        # Updated_on = date_today
        # print(Updated_on, "Updated_on")
        Cpu_model = _json['Cpu_model']
        print(Cpu_model, "Cpu_model")
        CPU_Sockets = _json['CPU_Sockets']
        print(CPU_Sockets, "CPU_Sockets")
        DIMM_Size = _json['DIMM_Size']
        print(DIMM_Size, "DIMM_Size")
        DIMM_Capacity = _json['DIMM_Capacity']
        # delete = dele.encode()
        print(DIMM_Capacity, "DIMM_Capacity")
        Storage_Vendor = _json['Storage_Vendor']
        print(Storage_Vendor, "Storage_Vendor")
        Storage_Controller = _json['Storage_Controller']
        print(Storage_Controller, "Storage_Controller")
        Storage_Capacity = _json['Storage_Capacity']
        print(Storage_Capacity, "Storage_Capacity")
        Network_Type = _json['Network_Type']
        print(Network_Type, "Network_Type")
        Network_speed = _json['Network_speed']
        print(Network_speed, "Network_speed")
        Number_Of_Network_Ports = _json['Number_Of_Network_Ports']
        print(Number_Of_Network_Ports, "Number_Of_Network_Ports")
        Special_Switching_Needs = _json['Special_Switching_Needs']
        print(Special_Switching_Needs, "Special_Switching_Needs")
        Infraadmin_Comments = _json['Infraadmin_Comments']
        print(Infraadmin_Comments, "Infraadmin_Comments")
        User_Comments = _json['User_Comments']
        print(User_Comments, "User_Comments")
        Request = _json['Request']
        print(User_Comments, "Request")

        # validate the received values
        if Id and User_No and Creator and Start_Date and End_Date and Manufacturer and \
                Number_Of_Servers and Operating_System and Cpu_model and CPU_Sockets and DIMM_Size and \
                DIMM_Capacity and Storage_Vendor and Storage_Controller and Storage_Capacity and \
                Network_Type and Network_speed and Number_Of_Network_Ports and \
                Special_Switching_Needs and Infraadmin_Comments and \
                User_Comments and Request and request.method == 'POST':  # giving condition whether the method is post

            query1 = ("SELECT Id FROM Server_Request ")  # qurey for selecting userid id from the usertable
            print(query1, "q1111")
            cursor.execute(query1)  # executing the qurey
            db224 = cursor.fetchall()  # fetching the qurey
            print(db224, "db224")
            usrid = []  # created an empty list for adding the user ids
            for i in db224:  # iterating the fetched values
                for j in i:  # iterating the tuples
                    print(usrid, "useridd")
                    usrid.append(j)  # appending the values in to the list
                print(usrid, "idddddd")

            query2 = ("SELECT User_Id FROM Users ")
            print(query2,"qqq2222222222222222")
            cursor.execute(query2)
            dbq2 = cursor.fetchall()
            print(dbq2,"dbq2")
            usid =[]
            for i in dbq2:
                for j in i:
                    print(usid,"usid")
                    usid.append(j)
                print(usid,"usssssssssss")

            if User_No not  in usid:  # checking the user id is present in the list
                resp = jsonify({"Message": "No current Requests!",
                                "Status": "400 Bad Request"})  # if the userid is present in the list it will show response as this
                resp.status_code = 400  # status code made as 400
                return resp  # this response will work if this condition works

            else:

                sql = "INSERT INTO Server_Request(Id,User_No, Creator, Start_Date,End_Date ,Manufacturer ," \
                      " Number_Of_Servers ,Operating_System, Cpu_model , CPU_Sockets, DIMM_Size," \
                      "DIMM_Capacity,Storage_Vendor,Storage_Controller,Storage_Capacity," \
                      "Network_Type,Network_speed," \
                      "Number_Of_Network_Ports,Special_Switching_Needs,Infraadmin_Comments,User_Comments,Request)" \
                      " VALUES(%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s,%s,%s,%s,%s,%s,%s)"  # qurey for inserting values to the sql
                print(sql, "sqlll")
                data = (Id,User_No, Creator, Start_Date, End_Date, Manufacturer, Number_Of_Servers,Operating_System, Cpu_model,
                        CPU_Sockets, DIMM_Size, DIMM_Capacity, Storage_Vendor, Storage_Controller, Storage_Capacity,
                      Network_Type, Network_speed,
                        Number_Of_Network_Ports, Special_Switching_Needs, Infraadmin_Comments, User_Comments,
                        Request)  # passing the variables from frondend to data
                print(data, "dataa")
                # connecting to psql

                cursor.execute(sql, data)  # executed the cursor with the sql qurey and the datas inserting
                conn.commit()  # commited the conn
                resp = jsonify(
                    {"Message": "Request added successfully!",
                     "Status": "200 OK"})  # created a response and jsonifed it
                return resp
            # resp.status_code = 200  # given a status code 200(truse) to the above response
            # return resp  # returning the response if the above condition works

        else:
            res = jsonify(
                {
                    "Message": "Request is not added please check the error below!"})
            res.status_code = 400  # giving error status
            return res

    except Exception as e:
        print(e)
    finally:
        cursor.close()


@app.route('/dashboard5', methods=['GET'])
def server_sorted():
    try:
        conn = connectDB()
        cursor = conn.cursor()
        conn.autocommit = True

        if request.method == 'GET':

            cursor.execute("(SELECT  DISTINCT '6 Months' AS time,(SELECT COUNT(*) FROM asset WHERE reserved='t' AND "
                           "EXTRACT(DAY FROM NOW() - assigned_from)<=182) AS no_of_reserved, (SELECT COUNT(*) FROM asset "
                           "WHERE reserved='f' AND EXTRACT(DAY FROM NOW() - assigned_from)<=182) AS no_of_vacant FROM asset"
                           " WHERE EXTRACT(DAY FROM NOW() - assigned_from)<=182) UNION (SELECT DISTINCT '1 Year' AS time,"
                           "(SELECT COUNT(*) FROM asset WHERE reserved='t' AND (EXTRACT(DAY FROM NOW() - assigned_from)> 182 AND"
                           " EXTRACT(DAY FROM NOW() - assigned_from)<=365)) AS no_of_reserved, (SELECT COUNT(*) FROM asset WHERE"
                           " reserved='f' AND (EXTRACT(DAY FROM NOW() - assigned_from)> 182 AND EXTRACT(DAY FROM NOW() - assigned_from)<=365))"
                           " AS no_of_vacant FROM asset WHERE (EXTRACT(DAY FROM NOW() - assigned_from)> 182 AND"
                           " EXTRACT(DAY FROM NOW() - assigned_from)<=365)) UNION (SELECT DISTINCT '1.5 Year' AS time,(SELECT COUNT(*) FROM "
                           "asset WHERE reserved='t' AND (EXTRACT(DAY FROM NOW() - assigned_from)> 365 AND EXTRACT(DAY FROM NOW() - assigned_from)<=574))"
                           " AS no_of_reserved, (SELECT COUNT(*) FROM asset WHERE reserved='f' AND (EXTRACT(DAY FROM NOW() - assigned_from)> 365 AND"
                           " EXTRACT(DAY FROM NOW() - assigned_from)<=574)) AS no_of_vacant FROM asset WHERE (EXTRACT(DAY FROM NOW() - assigned_from)> 365"
                           " AND EXTRACT(DAY FROM NOW() - assigned_from)<=574)) UNION (SELECT DISTINCT '2 Years' AS time,(SELECT COUNT(*) FROM"
                           " asset WHERE reserved='t' AND (EXTRACT(DAY FROM NOW() - assigned_from)>574)) AS no_of_reserved, (SELECT COUNT(*) FROM asset WHERE "
                           "reserved='f' AND (EXTRACT(DAY FROM NOW() - assigned_from)>574)) AS no_of_vacant FROM asset WHERE "
                           "(EXTRACT(DAY FROM NOW() - assigned_from)>574));")

            c = cursor.fetchall()
            dashboard = []
            print(c, "ccccccccccccccccc")
            for i in c:
                lst = list(i)
                dashboard.append({"Timeline": lst[0], "reserved": lst[1], "vacant": lst[2]})
            print(dashboard)
        return jsonify({"Dashboard": dashboard[::-1], "Message": "Updated Statistics", "Status": "200 OK"})
    except Exception as e:
        print(e)
    finally:
        cursor.close()


@app.route('/my_request', methods=['POST'])
def getMyRequest():
    """"""
    try:
        conn = connectDB()
        cursor = conn.cursor()
        cursor.execute("select User_No from Server_Request")
        result = cursor.fetchall()
        list_user_id = []
        for i in result:
            for j in i:
                list_user_id.append(j)
        print(list_user_id)

        User_No = request.json.get('User_No')
        print(User_No)
        print(type(User_No))
        cursor1 = conn.cursor()


        if int(User_No) in list_user_id:
            query = "select *  from Server_Request where User_No=%s"
            cursor1.execute(query, [User_No])
            res = cursor1.fetchall()
            print(res, "ressssss")
            # arr = [desc[0] for desc in cursor1.description]  # getting column name from database

            arr = ["Id","User_No", "Creator", "Start_Date", "End_Date", "Manufacturer", "Number_Of_Servers", "Operating_System",
                   "Cpu_model", "CPU_Sockets", "DIMM_Size", "DIMM_Capacity", "Storage_Vendor", "Storage_Controller",
                   "Storage_Capacity", "Network_Type", "Network_speed", "Number_Of_Network_Ports",
                   "Special_Switching_Needs", "Infraadmin_Comments", "User_Comments", "Request"]

            json_data = convert_json(res, arr)

            return jsonify(
                {"ListMyRequests": json_data, "Message": "Listed specified requests", "Status Code": "200 OK"})
        else:
            resp = jsonify({"Message": "Request not found", "Status Code": "202 "})
            resp.status_code = 400
            return resp
    except Exception as e:
        print(e)
        resp = jsonify({"Message": str(e), "Status Code": "202"})
        resp.status_code = 202
        return resp


##################################################################################################################

@app.route('/view-users/<id>')
def user(id):  # created a function an passing id as an argument because this id is calling in the url
    conn = connectDB()  # connecting to the database
    cursor = conn.cursor(cursor_factory=RealDictCursor)  # the database is connection is given to a cursor
    cursor.execute(
        "SELECT User_Id User_Id, Email_Id Email_Id, Password Password,First_Name First_Name,Last_Name Last_Name,Created_on Created_on,"
        "created_by created_by,Updated_on Updated_on,Updated_by Updated_by, Role Role,Teams Teams  FROM Users WHERE User_Id=%s",
        (id,))  # qurey for selecting the userid
    row = cursor.fetchone()  # fetching the datas of that corresponding id
    resp = jsonify(row)  # jsonifying the datas
    resp.status_code = 200  # giving the response status as 200 if the above condition works
    return resp


@app.route('/delete-permanent/<id>', methods=['DELETE'])
def permanently_delete(id):  # created a function for deleting user with their corresponding
    # id so thats why the id passing as an argument it will call in the url
    id = (id)
    conn = connectDB()  # connecting to the database
    cursor = conn.cursor(
        cursor_factory=RealDictCursor)  # created a cursor function and giving cursor_factory=RealDictCursor

    cursor.execute("SELECT * FROM Users WHERE User_Id=%s", (id,))  # qurey for selecting the datas with the given id
    # and given to the cursor and it will execute
    db22 = cursor.fetchall()  # fetching all the datas of that corresponding id
    print(db22, "db22")
    if len(db22) != 0:  # checking condition if the user is not null
        cursor.execute("DELETE FROM Users WHERE User_Id=%s", id)  # qurey for deleting and it will
        # work only the value is not equal to null
        conn.commit()
        resp = jsonify('User deleted successfully!')  # response is jsonifying
        resp.status_code = 200  # giving status code as 200 (true)
        return resp  # if the above condition works thengive the response as 200
    else:
        res = jsonify("User not available with  id ", id)  # if the user is null then this response works
        res.status_code = 400  # error response
        return res


@app.route('/sort', methods=['GET'])
def sort():
    test_list = ['gfg', 1, 2, 'is', 'best']

    # printing original list
    print("The original list : " + str(test_list))
    # res_str = [ele for ele in test_list if isinstance(ele, str)]
    # res_int = [ele for ele in test_list if isinstance(ele, int)]
    #
    # # printing result
    # print("Integer list : " + str(res_int))
    # print("String list : " + str(res_str))
    currentMonth = datetime.datetime.now().month
    currentYear = datetime.datetime.now().year
    month_start_date = datetime.datetime(currentYear, currentMonth, 1)
    print(month_start_date, "monnnnnnnnnnnnnnnnth")
    todays_date = date.today()
    print(todays_date, "todattyyyyy")
    # start = datetime.datetime.strptime(request.POST["start_time"], '%H:%M:%S.%f').time()
    # print(start,"starrrrrrr")
    end = datetime.datetime.now().time()
    print(end, "enddd")
    # duration = datetime.datetime.combine(date.today(), end) - datetime.datetime.combine(date.today(), start)
    # print(duration,"durationnnnnnnnnnnnnnnnnn")
    # try:
    conn = connectDB()
    cursor = conn.cursor()
    conn.autocommit = True
    cursor.execute(
        "SELECT Asset_Id,Assigned_from ::timestamp::date,NOW()::timestamp::date,EXTRACT(DAY FROM NOW() - assigned_from) AS Days FROM asset;")
    fff = cursor.fetchall()
    print(fff, "ffffffffff")

    if request.method == 'GET':  # GET method is used here
        cursor.execute('select assigned_from from asset ORDER BY created_on ASC')  # store inserver_table
        data = cursor.fetchall()  # crusor fetchs all the data
        # print(date_today,"dateeeeeeeeeeeeeeeeeeee")
        # l = (data[0][0]).days/182
        # print(l,"9999999999999")

        n = (datetime.datetime.now() - data[0][0]).days / 182
        print(n, 'nnnnnnnnnnnnnnnnn')
        n = int(n)
        n += 1
        required = []
        for i in range(1, n):
            m = i * 182
            k = (i + 1) * 182
            start = datetime.date.today() - datetime.timedelta(days=m)
            end = datetime.date.today() - datetime.timedelta(days=k)
            if i == 1:
                cursor.execute(
                    "select assigned_from,asset_id,reserved from asset where created_on >= '" + str(start) + "'")
            else:
                cursor.execute("select assigned_from,asset_id,reserved from asset where created_on between '" + str(
                    end) + "' and '" + str(start) + "'")
            d = cursor.fetchall()
            dic = {}
            dic['time'] = 'Less than ' + str(i * 6) + ' months'
            dic['total'] = len(d)
            dic['data'] = d
            required.append(dic)
        print(required)
        return jsonify(
            {"Message": "Record found", "Status code": '200 OK', "dashboard": required})


"""View all the users present in the database"""
# @app.route('/view_users')
# def list_users():
#     conn = connectDB()  # connecting to database
#     cursor = conn.cursor(
#         cursor_factory=RealDictCursor)  # created a cursor and connected with the db and giving cursor_factory as
#     # RealDictCursor for getting it as key value pair
#     cursor.execute(
#         "SELECT User_Id, Email_Id, First_Name, Last_Name, Created_on, created_by,Updated_on,Updated_by,Role,Teams FROM Users")  # given a qurey inside the execute function
#     rows = cursor.fetchall()  # fetching all from the cursor
#     for i in rows:
#         # print(i,"uuuuuuuu")
#         for j in i:
#             print(j,"jjjjj")
#     # print(rows,"rowssss")
#     resp = jsonify({"Message": "Record found", "Status": "200 OK","List users":rows})
#     # resp = jsonify({rows})  # jsonifying the fetched data from the database
#     resp.status_code = 200  # if the above condition works then given status code as 200
#     return resp  # returning the response


# @app.route('/sortin', methods=['GET'])
# def sorting():
#     currentMonth = datetime.datetime.now().month
#     currentYear = datetime.datetime.now().year
#     month_start_date = datetime.datetime(currentYear, currentMonth, 1)
#     print(month_start_date, "monnnnnnnnnnnnnnnnth")
#     todays_date = date.today()
#     print(todays_date, "todattyyyyy")
#     # start = datetime.datetime.strptime(request.POST["start_time"], '%H:%M:%S.%f').time()
#     # print(start,"starrrrrrr")
#     end = datetime.datetime.now().time()
#     print(end, "enddd")
#     # duration = datetime.datetime.combine(date.today(), end) - datetime.datetime.combine(date.today(), start)
#     # print(duration,"durationnnnnnnnnnnnnnnnnn")
#     # try:
#     conn = connectDB()
#     print(conn, "kkkkkk")
#     cursor = conn.cursor()
#     conn.autocommit = True
#
#     if request.method == 'GET':  # GET method is used here
#         cursor.execute('select created_on from asset')  # store inserver_table
#         data = cursor.fetchall()  # crusor fetchs all the data
#         # print(date_today,"dateeeeeeeeeeeeeeeeeeee")
#         print(data, "dddddddddddddddddddddddddddddddddddddddddddddddd")
#         user = []  # serverlist for get method with variable serverl
#         for i in data:
#             for j in i:
#                 user.append(j)
#                 print(j, "jjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
#                 print(user, "ooooooooooooo")
#
#         date_month = []
#         print(user, "uuuuuuuuuuuuuuuuuuuuuuuuuuuu")
#         for i in user:
#             print(type(i), "typeeeeeeeeeeee", i)
#             l = datetime.datetime.now() - (i)
#             six_months = date.today() + relativedelta(months=+6)
#             # print(six_months, "sixxmonth")
#             print(l, "llllllllllll")
#             # print("90", str(i))
#             # print("9222", str(60))
#             # print(i,"iiiiiiiii")
#             # if i in user:
#             lessthan6 = []
#             excact6 = []
#             morethan6 = []
#             oneyear = []
#
#             if str(l) < "181days,00:00:00.00":
#                 # print("less than 6 month")
#                 # six_months.append(str(l))
#                 lessthan6.append(l)
#                 print("less than 6 months", lessthan6)
#                 # lessthan6 = {"dates": str(date_month)}
#                 # return jsonify({"Message": "Record found", "Status code": '200 OK', "Listusers": lessthan6})
#
#             elif str(l) == "181days,00:00:00.00":
#                 # print("excact 6 month")
#                 excact6.append(l)
#                 print("excact 6 month", excact6)
#                 # excact6 = {"dates": str(date_month)}
#                 # return jsonify({"Message": "Record found", "Status code": '200 OK', "Listusers": excact6})
#
#
#
#             elif str(l) >= "181days,00:00:00.00":
#                 # print("more than 6 months")
#                 morethan6.append(l)
#                 print("morethan 6 month", morethan6)
#                 # morethan6 = {"dates": str(date_month)}
#                 # return jsonify({"Message": "Record found", "Status code": '200 OK', "Listusers": morethan6})
#
#             elif str(l) == "365days,00:00:00.00":
#                 # print("1 year")
#                 oneyear.append(l)
#                 print("1 year", oneyear)
#                 # oneyear = {"dates": str(date_month)}
#                 # return jsonify({"Message": "Record found", "Status code": '200 OK', "Listusers": oneyear})
#         return jsonify(
#             {"Message": "Record found", "Status code": '200 OK', "lessthan6": str(lessthan6), "excact6": str(excact6),
#              "morethan6": str(morethan6), "oneyear": str(oneyear)})
#
#         # print(i,"iiiiiii")
#         # print(date_time,"timmmmmmm")
#     #             jsonData = {"User_Id": userdata[0], "Email_Id": userdata[1], "Password": userdata[2],
#     #                         "First_Name": userdata[3], "Last_Name": userdata[4], "Created_on": userdata[5],
#     #                         "Created_by": userdata[6], "Updated_on": userdata[7], "Updated_by": userdata[8],
#     #                         "Role": userdata[9], "Teams": userdata[10], "Delete": userdata[11],
#     #                         }
#     #             user.append(jsonData)  # it will show all the data stored in the database with key:value
#     #         data_user = []
#     #             for i in user:
#     #                 if i["Created_on"]:
#     #                     created_date = i["Created_on"]
#     #                     date_time_obj = created_date.isoformat() + 'Z'
#     #                     i.update({"Created_on": date_time_obj})
#     #                 if i["Updated_on"]:
#     #                     Updated_date = i["Updated_on"]
#     #                     date_time_obj1 = Updated_date.isoformat() + 'Z'
#     #                     i.update({"Updated_on": date_time_obj1})
#     #                 data_user.append(i)
#     #                 print("datauserrr",data_user)
#     #     return jsonify({"Message": "Record found", "Status code": '200 OK', "Listusers": data_user})
#     #
#     # except Exception as e:
#     #     print(e)
#     # finally:
#     #     cursor.close()
#
#
# @app.route('/sorting', methods=['GET'])
# def sortig():
#     test_list = ['gfg', 1, 2, 'is', 'best']
#
#     # printing original list
#     print("The original list : " + str(test_list))
#     # res_str = [ele for ele in test_list if isinstance(ele, str)]
#     # res_int = [ele for ele in test_list if isinstance(ele, int)]
#     #
#     # # printing result
#     # print("Integer list : " + str(res_int))
#     # print("String list : " + str(res_str))
#     currentMonth = datetime.datetime.now().month
#     currentYear = datetime.datetime.now().year
#     month_start_date = datetime.datetime(currentYear, currentMonth, 1)
#     print(month_start_date, "monnnnnnnnnnnnnnnnth")
#     todays_date = date.today()
#     print(todays_date, "todattyyyyy")
#     # start = datetime.datetime.strptime(request.POST["start_time"], '%H:%M:%S.%f').time()
#     # print(start,"starrrrrrr")
#     end = datetime.datetime.now().time()
#     print(end, "enddd")
#     # duration = datetime.datetime.combine(date.today(), end) - datetime.datetime.combine(date.today(), start)
#     # print(duration,"durationnnnnnnnnnnnnnnnnn")
#     # try:
#     conn = connectDB()
#     cursor = conn.cursor()
#     conn.autocommit = True
#     lessthan6 = []
#     excact6 = []
#     morethan6 = []
#     oneyear = []
#
#     if request.method == 'GET':  # GET method is used here
#         cursor.execute('select created_on from asset')  # store inserver_table
#         data = cursor.fetchall()  # crusor fetchs all the data
#         # print(date_today,"dateeeeeeeeeeeeeeeeeeee")
#         print(data, "dddddddddddddddddddddddddddddddddddddddddddddddd")
#         user = []  # serverlist for get method with variable serverl
#         for i in data:
#             for j in i:
#                 user.append(j)
#                 # print(int(j), "jjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
#         # print(user, "ooooooooooooo")
#         #
#         # date_month = []
#
#         for i in user:
#             print(type(i), "typeeeeeeeeeeee", i)
#             res_str = [ele for ele in user if isinstance(ele, datetime.datetime)]
#             res_int = [ele for ele in user if isinstance(ele, int)]
#             print("Integer list : " + str(res_int))
#             print("String list : " + str(res_str))
#             l = datetime.datetime.now() - (i)
#             #     six_months = date.today() + relativedelta(months=+6)
#             #     # print(six_months, "sixxmonth")
#             print(l, "llllllllllll")
#             #     # print("90", str(i))
#             #     # print("9222", str(60))
#             #     # print(i,"iiiiiiiii")
#             #     # if i in user:
#
#             #
#             if str(l) < "181days,00:00:00.00":
#                 # print("less than 6 month")
#                 # six_months.append(str(l))
#                 lessthan6.append(l)
#                 # print("less than 6 months", lessthan6)
#             #         # lessthan6 = {"dates": str(date_month)}
#             #         # return jsonify({"Message": "Record found", "Status code": '200 OK', "Listusers": lessthan6})
#             #
#             elif str(l) == "181days,00:00:00.00":
#                 #         # print("excact 6 month")
#                 excact6.append(l)
#             #         print("excact 6 month", excact6)
#             #         # excact6 = {"dates": str(date_month)}
#             #         # return jsonify({"Message": "Record found", "Status code": '200 OK', "Listusers": excact6})
#             #
#             #
#             #
#             elif str(l) >= "181days,00:00:00.00":
#                 #         # print("more than 6 months")
#                 morethan6.append(l)
#             #         print("morethan 6 month", morethan6)
#             #         # morethan6 = {"dates": str(date_month)}
#             #         # return jsonify({"Message": "Record found", "Status code": '200 OK', "Listusers": morethan6})
#             #
#             elif str(l) == "365days,00:00:00.00":
#                 #         # print("1 year")
#                 oneyear.append(l)
#         #         print("1 year", oneyear)
#         #         # oneyear = {"dates": str(date_month)}
#         #         # return jsonify({"Message": "Record found", "Status code": '200 OK', "Listusers": oneyear})
#     return jsonify(
#         {"Message": "Record found", "Status code": '200 OK', "lessthan6": str(lessthan6), "excact6": str(excact6),
#          "morethan6": str(morethan6), "oneyear": str(oneyear)})
#     # return jsonify(result = str(lessthan6))
#     # return Response(json.dumps(lessthan6))
#
# @app.route('/sort', methods=['GET'])
# def sort():
#     test_list = ['gfg', 1, 2, 'is', 'best']
#
#     # printing original list
#     print("The original list : " + str(test_list))
#     # res_str = [ele for ele in test_list if isinstance(ele, str)]
#     # res_int = [ele for ele in test_list if isinstance(ele, int)]
#     #
#     # # printing result
#     # print("Integer list : " + str(res_int))
#     # print("String list : " + str(res_str))
#     currentMonth = datetime.datetime.now().month
#     currentYear = datetime.datetime.now().year
#     month_start_date = datetime.datetime(currentYear, currentMonth, 1)
#     print(month_start_date, "monnnnnnnnnnnnnnnnth")
#     todays_date = date.today()
#     print(todays_date, "todattyyyyy")
#     # start = datetime.datetime.strptime(request.POST["start_time"], '%H:%M:%S.%f').time()
#     # print(start,"starrrrrrr")
#     end = datetime.datetime.now().time()
#     print(end, "enddd")
#     # duration = datetime.datetime.combine(date.today(), end) - datetime.datetime.combine(date.today(), start)
#     # print(duration,"durationnnnnnnnnnnnnnnnnn")
#     # try:
#     conn = connectDB()
#     cursor = conn.cursor()
#     conn.autocommit = True
#     cursor.execute(
#         "SELECT Asset_Id,Assigned_from ::timestamp::date,NOW()::timestamp::date,EXTRACT(DAY FROM NOW() - assigned_from) AS Days FROM asset;")
#     fff = cursor.fetchall()
#     print(fff, "ffffffffff")
#
#     if request.method == 'GET':  # GET method is used here
#         cursor.execute('select assigned_from from asset ORDER BY created_on ASC')  # store inserver_table
#         data = cursor.fetchall()  # crusor fetchs all the data
#         # print(date_today,"dateeeeeeeeeeeeeeeeeeee")
#         # l = (data[0][0]).days/182
#         # print(l,"9999999999999")
#
#         n = (datetime.datetime.now() - data[0][0]).days / 182
#         print(n, 'nnnnnnnnnnnnnnnnn')
#         n = int(n)
#         n += 1
#         required = []
#         for i in range(1, n):
#             m = i * 182
#             k = (i + 1) * 182
#             start = datetime.date.today() - datetime.timedelta(days=m)
#             end = datetime.date.today() - datetime.timedelta(days=k)
#             if i == 1:
#                 cursor.execute(
#                     "select assigned_from,asset_id,reserved from asset where created_on >= '" + str(start) + "'")
#             else:
#                 cursor.execute("select assigned_from,asset_id,reserved from asset where created_on between '" + str(
#                     end) + "' and '" + str(start) + "'")
#             d = cursor.fetchall()
#             dic = {}
#             dic['time'] = 'Less than ' + str(i * 6) + ' months'
#             dic['total'] = len(d)
#             dic['data'] = d
#             required.append(dic)
#         print(required)
#         return jsonify(
#             {"Message": "Record found", "Status code": '200 OK', "dashboard": required})
#     # print(n, "nnnnnnnnnnnnnnnnnnnnnnnnnn")
#         # largest = data[length][0]
#         # print(largest, 'largestlargestlargestlargestlargestlargest')
#     #     user = []  # serverlist for get method with variable serverl
#     #     for i in data:
#     #         for j in i:
#     #             user.append(j)
#     #             # print(int(j), "jjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
#     #     # print(user, "ooooooooooooo")
#     #     #
#     #     # date_month = []
#     #
#     #
#     #     for i in user:
#     #         # print(type(i), "typeeeeeeeeeeee", i)
#     #         res_date = [ele for ele in user if isinstance(ele, datetime.datetime)]
#     #         res_int = [ele for ele in user if isinstance(ele, int)]
#     #         # print("Integer list : " + str(res_int))
#     #         # print("Date list : " + str(res_date))
#     #
#     #         lessthan6 = []
#     #         excact6 = []
#     #         morethan6 = []
#     #         oneyear = []
#     #         for j in res_date:
#     #             l = datetime.datetime.now() - (j)
#     #         #     six_months = date.today() + relativedelta(months=+6)
#     #         #     # print(six_months, "sixxmonth")
#     #         #     print(l, "llllllllllll")
#     #     #     # print("90", str(i))
#     #     #     # print("9222", str(60))
#     #     #     # print(i,"iiiiiiiii")
#     #     #     # if i in user:
#     #
#     #     #
#     #
#     #             if str(l) < "181days,00:00:00.00":
#     #                 # print("less than 6 month")
#     #                 # six_months.append(str(l))
#     #                 lessthan6.append(l)
#     #                 # print("less than 6 months", lessthan6)
#     #         #         # lessthan6 = {"dates": str(date_month)}
#     #         #         # return jsonify({"Message": "Record found", "Status code": '200 OK', "Listusers": lessthan6})
#     #         #
#     #             elif str(l) == "181days,00:00:00.00":
#     #         #         # print("excact 6 month")
#     #                 excact6.append(l)
#     #         #         print("excact 6 month", excact6)
#     #         #         # excact6 = {"dates": str(date_month)}
#     #         #         # return jsonify({"Message": "Record found", "Status code": '200 OK', "Listusers": excact6})
#     #         #
#     #         #
#     #         #
#     #             elif str(l) >= "181days,00:00:00.00":
#     #         #         # print("more than 6 months")
#     #                 morethan6.append(l)
#     #         #         print("morethan 6 month", morethan6)
#     #         #         # morethan6 = {"dates": str(date_month)}
#     #         #         # return jsonify({"Message": "Record found", "Status code": '200 OK', "Listusers": morethan6})
#     #         #
#     #             elif str(l) == "365days,00:00:00.00":
#     #         #         # print("1 year")
#     #                 oneyear.append(l)
#     #         #         print("1 year", oneyear)
#     #         #         # oneyear = {"dates": str(date_month)}
#     #        #         # return jsonify({"Message": "Record found", "Status code": '200 OK', "Listusers": oneyear})
#     # # print(lessthan6,"lessthan6")
#     # # print(excact6,"excact6")
#     # # print(morethan6,"morethan6")
#     # # print(oneyear,"oneyear")
#     #
#     # return jsonify(
#     # {"Message": "Record found", "Status code": '200 OK', "lessthan6": str(lessthan6), "excact6": str(excact6),
#     #  "morethan6": str(morethan6), "oneyear": str(oneyear)})
#     # return jsonify(result = str(lessthan6))
#     # return Response(json.dumps(lessthan6))

"""deleting user (changing the delete as 0) """
# @app.route('/Delete_Role/<id>', methods=['PUT'])
# def delete_user(id):  # created a function for deleting user with their corresponding
#     # id so thats why the id passing as an argument it will call in the url
#     id = int(id)
#     print(id, "id")
#
#     conn = connectDB()  # connecting to the database
#     cursor = conn.cursor()  # created a cursor function and giving cursor_factory=RealDictCursor
#
#     cursor.execute("SELECT * FROM Users  WHERE User_Id=%s", (id,))  # qurey for selecting the datas with the given id
#     # and given to the cursor and it will execute
#     db22 = cursor.fetchall()  # fetching all the datas of that corresponding id
#     print(db22, "db22")
#     """test"""
#     query1 = "SELECT User_Id FROM Users WHERE DELETE ='0' ;"
#     print(query1, "qqq1111")
#     cursor.execute(query1)
#     db33 = cursor.fetchall()
#     print(db33, "db3333333333")
#     dele = []
#     for i in db33:
#         # print(i,"iii")
#         for j in i:
#             # print(j,"jjjj")
#             dele.append(j)
#     print(dele, "dele")
#     if id in dele:
#         print("its already deleted")
#         res = jsonify('This is already deleted!')  # jsonifying the response
#         res.status_code = 400  # giving status code 400 (False)
#         return res
#
#     """endtest"""
#     if len(db22) != 0:  # checking condition if the user is not null
#         cursor.execute("UPDATE  Users SET DELETE ='0'WHERE User_Id =%s", (id,))  # qurey for deleting and it will
#         # work only the value is not equal to null
#         conn.commit()
#         resp = jsonify('User deleted successfully!')  # response is jsonifying
#         resp.status_code = 200  # giving status code as 200 (true)
#         return resp  # if the above condition works thengive the response as 200
#     else:
#         res = jsonify("User not available with  id ", id)  # if the user is null then this response works
#         res.status_code = 400  # error response
#         return res

#
# """Updating users"""
# @app.route('/Update_Role', methods=['PUT'])
# def update_User():
#     _json = request.json  # converting the request to json
#     User_Id = _json['User_Id']
#     print(User_Id, "User_Id")
#     # Email_Id = _json['Email_Id']
#     # print(Email_Id, "Email_Id")
#     # Password = _json['Password']
#     # print(Password, "PASSSWORD")
#     First_Name = _json['First_Name']
#     print(First_Name, "First_Name")
#     Last_Name = _json['Last_Name']
#     print(Last_Name, "Last_Name")
#     # Created_on = date_today
#     # print(Created_on, "Created_on")
#     # Created_by = _json['Created_by']
#     # print(Created_by, "Created_by")
#     Updated_on = date_today
#     print(Updated_on, "Updated_on")
#     Updated_by = _json['Updated_by']
#     print(Updated_by, "Updated_by")
#     Role = _json['Role']
#     print(Role, "Role")
#     Teams = _json['Teams']
#     print(Teams, "Teams")
#     # Delete = _json['Delete']
#     # # delete = dele.encode()
#     # print(Delete, "deletee", Delete)
#
#     # validate the received values
#     if User_Id and First_Name and Last_Name and \
#              Updated_on and Updated_by and Role and Teams  and request.method == 'PUT':
#         _hashed_password = generate_password_hash(Password)  # do not save password as a plain text so the
#         # generate_password_hash will encrypt the password
#         # save edits
#         sql = "UPDATE Users SET  First_Name = %s," \
#               " Last_Name = %s, Updated_on = %s,Updated_by=%s, Role=%s, Teams=%s,  WHERE User_Id=%s "  # qurey for updating
#         print(sql, "sqlllllll")
#         data = (
#         _hashed_password, First_Name, Last_Name, Created_on, Created_by, Updated_on, Updated_by, Role, Teams, Delete,
#         User_Id
#         )  # taking the datas from frondend and passing in to a variable
#         print(data, "dataaa")
#         conn = connectDB()  # connecting to the database
#         cursor = conn.cursor()
#         query1 = "SELECT User_Id FROM Users"  # qurey for selecting email id from the usertable
#         print(query1, "qq11")
#         cursor.execute(query1)  # executing the qurey
#         db223 = cursor.fetchall()  # fetching the qurey
#         print(db223, "db22")
#         userid = []  # created an empty list for adding the email ids
#
#         for i in db223:  # iterating the fetched values
#             for j in i:  # iterating the tuples
#                 userid.append(j)
#         print(userid, "userrr")
#         if User_Id in userid:
#             cursor.execute(sql, data)  # executing the qurey and the datas from frond end
#             conn.commit()
#             resp = jsonify('User updated successfully!')  # jsonifying the response
#             resp.status_code = 200  # making the status as 200 (true)
#             conn.close()
#             return resp  # if the above condition works then giving the response 200
#         else:
#             resp = jsonify(
#                 'no userid!')  # if the userid is present in the list it will show response as this
#             resp.status_code = 400  # status code made as 400
#             return resp
#     else:
#         res = jsonify('User not found')  # jsonifying the response
#         res.status_code = 400  # giving status code 400 (False)
#         return res  # returning the response
#


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
