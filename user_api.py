from flask import Flask, jsonify, request
from Connect2DB import *
from datetime import date
import flask.json

dbase = connectDB()
dbase.autocommit = True  # commits every transaction to database automatically
app = Flask(__name__)


# function to convert json format from list of tuples and array.
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


@app.route('/list_asset/reserved', methods=['GET'])
def list_all_reserved():
    try:
        cursor = dbase.cursor()
        # To show reserved servers,fetch all the data base from the asset table where reserved=false.
        cursor.execute(
            "select asset_id,manufacturer,bmc_ip,bmc_user,asset_location,assigned_to,assigned_from,assigned_by,created_on,created_by,updated_on,updated_by,purpose,cluster_id from asset where reserved=true")
        res = cursor.fetchall()
        print(res)
        arr = [desc[0] for desc in cursor.description]  # getting column name from database
        json_data = convert_json(res, arr)
        # if json.args()
        return jsonify(json_data)
    except Exception as e:
        print(e)
    finally:
        cursor.close()


@app.route('/list_asset/pool', methods=['GET'])
def list_all_pool():
    try:
        cursor = dbase.cursor()
        # To show reserved servers,fetch all the data base from the asset table where reserved=false.
        cursor.execute(
            "select asset_id,manufacturer,bmc_ip,bmc_user,asset_location,assigned_to,assigned_from,assigned_by,created_on,created_by,updated_on,updated_by,purpose,cluster_id from asset where reserved=false")
        res = cursor.fetchall()
        print(res)
        arr = [desc[0] for desc in cursor.description]  # getting column name from database
        json_data = convert_json(res, arr)

        return jsonify(json_data)
    except Exception as e:
        print(e)
    finally:
        cursor.close()


# @app.route('/update_asset_table', methods=['PUT'])
# def update_user():
#     try:
#         cursor = dbase.cursor()
#         # taking details from the parameters passed in url.
#         asset_id = request.json.get('asset_id')
#         location = request.json.get('asset_location')
#         # team = request.json.get('teams')
#         purpose = request.json.get('purpose')
#         # query to update server in the database.
#         query = "UPDATE asset SET asset_location=%s, purpose=%s WHERE asset_id=%s"
#         data = (location, purpose, asset_id)
#         cursor.execute(query, data)
#
#         return "details updated successfully!"
#
#     except Exception as e:
#         return jsonify(e)
#
#     finally:
#         cursor.close()


@app.route('/my_server', methods=['GET'])
def my_server():
    try:
        cursor = dbase.cursor()
        cursor.execute("select user_id from users")
        result = cursor.fetchall()
        list_user_id = []
        for i in result:
            for j in i:
                list_user_id.append(j)
        print(list_user_id)

        user_id = request.json.get('user_id')
        print(user_id)
        print(type(user_id))
        cursor1 = dbase.cursor()
        if int(user_id) in list_user_id:
            query = "select * from asset where reserved=%s and assigned_to=%s"
            cursor1.execute(query, [True, user_id])
            res = cursor1.fetchall()
            arr = [desc[0] for desc in cursor1.description]  # getting column name from database
            json_data = convert_json(res, arr)
            return jsonify(json_data)
        else:
            return jsonify({"error": "Invalid user_id"})
    except Exception as e:
        error = {"error": e}
        return jsonify(error)
    finally:
        cursor1.close()


@app.route('/release_asset', methods=['PUT'])
def release():
    try:
        cursor = dbase.cursor()
        asset_id = request.json.get('asset_id')
        cursor.execute("select reserved from asset where asset_id=%s", [asset_id])
        res = cursor.fetchall()
        print(res)
        for i in res:
            for j in i:
                if j:
                    cursor1 = dbase.cursor()
                    cursor1.execute(
                        "update asset set assigned_to=NULL,assigned_from=NULL,assigned_by=NULL,status = %s,reserved=%s where asset_id=%s",
                        [False, False, asset_id])
                    cursor1.execute(
                        "select assigned_to,assigned_from,updated_on,updated_by from asset where asset_id=%s",
                        [asset_id])
                    details = cursor1.fetchall()
                    for item in details:
                        assigned_to = item[0]
                        assigned_from = item[1]
                        updated_on = item[2]
                        updated_by = item[3]
                    cursor1.execute("select id from historic_details")
                    res1 = cursor1.fetchall()
                    l = []
                    for ii in res1:
                        for jj in ii:
                            l.append(jj)
                    l.sort()
                    id = l[-1] + 1
                    cursor1.execute(
                        "INSERT INTO Historic_details(ID,Asset_ID,Assigned_to,Assigned_from,Updated_on,Updated_by,Remarks) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                        [id, asset_id, assigned_to, assigned_from, updated_on, updated_by, 'releasing asset'])

                    return jsonify({"status 200": "server released!"})

                else:
                    return jsonify({"StatusInternalServerError": "Invalid character 400",
                                    "message": "server already released!!"})
    except Exception as e:
        print(e)
        return jsonify({"StatusInternalServerError": "Invalid character 400"})


@app.route('/assign_asset', methods=['PUT'])
def assign():
    try:
        cursor = dbase.cursor()
        # getting asset id and user id from input parameters
        asset_id = request.json.get('asset_id')
        user_id = request.json.get('user_id')
        cursor1 = dbase.cursor()
        cursor.execute("select reserved from asset where asset_id=%s", [asset_id])
        res = cursor.fetchall()
        # cursor1.execute("select id from historic_details")
        # res1 = cursor1.fetchall()
        # l = []
        # for i in res1:
        #     for j in i:
        #         l.append(j)
        # l.sort()
        # id = l[-1] + 1

        for i in res:
            for j in i:
                if j:
                    return jsonify({"Message": "server already assigned!", "Status Code": "400 Bad Request"})
                else:
                    cursor1.execute("select id from historic_details")
                    res1 = cursor1.fetchall()
                    l = []
                    for ii in res1:
                        for jj in ii:
                            l.append(jj)
                    l.sort()
                    id = l[-1] + 1
                    cursor1.execute("select Updated_on,Updated_by from asset where asset_id=%s", [asset_id])
                    resultt = cursor1.fetchall()
                    for data in resultt:
                        Updated_on = data[0]
                        Updated_by = data[1]
                    cursor1.execute(
                        "INSERT INTO Historic_details(ID,Asset_ID,Assigned_to,Assigned_from,Updated_on,Updated_by,Remarks) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                        [id, asset_id, user_id, date.today(), Updated_on, Updated_by, 'assigning server'])
                    cursor1.execute(
                        "update asset set assigned_to=%s,assigned_from=%s, assigned_by=%s,status=%s,reserved=%s where asset_id=%s",
                        [user_id, date.today(), user_id, True, True, asset_id])
                    return jsonify({"Message": "Server Assigned!", "Status Code": "200 OK"})
    except Exception as e:
        print(e)
        return jsonify({"Message": e, "Status Code": "400 Bad Request"})

#
# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=5000, debug=True)

if __name__ == '__main__':
    app.run(debug=True)