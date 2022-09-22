import datetime as datetime
from datetime import date

from flask import Flask, request
from flask import jsonify
from flask_cors import CORS, cross_origin
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash

from connect2DB import *
from datetime import date
from dateutil.relativedelta import relativedelta

date_today = date.today()
date_time = datetime.datetime.now()
d = datetime.datetime.strptime('2011-06-09', '%Y-%m-%d')
my_datetime_utc = date_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')

app = Flask(__name__)
CORS(app)

@app.route('/delete_user', methods=['GET'])
def delete_user():  # created a function for deleting user with their corresponding
    # try:
        # id so thats why the id passing as an argument it will call in the url
        # id = int(id)
        # print(id, "id")
        # _json = request.get  # converting the request to json
        # User_Id = _json['User_Id']
        User_Id =request.args.get("User_Id")
        print(User_Id, "User_Id")

        conn = connectDB()  # connecting to the database
        cursor = conn.cursor()  # created a cursor function and giving cursor_factory=RealDictCursor

        cursor.execute("SELECT * FROM Users  WHERE User_Id=%s",
                       (User_Id,))  # qurey for selecting the datas with the given id
        # and given to the cursor and it will execute
        db22 = cursor.fetchall()  # fetching all the datas of that corresponding id
        print(db22, "db22")
        """test"""
        # "SELECT User_Id FROM Users WHERE DELETE ='1' ;"
        # query1 = ("SELECT delete FROM Users WHERE User_Id=%s", User_Id)
        # print(query1, "qqq1111")
        # cursor.execute(query1)
        cursor.execute("SELECT delete FROM Users  WHERE User_Id=%s",
                       (User_Id,))
        db33 = cursor.fetchall()
        print(db33, "db3333333333")
        dele = []
        for i in db33:
            # print(i,"iii")
            for j in i:
                # print(j,"jjjj")
                dele.append(j)

        print(dele, "dele")
        return jsonify({"message":dele[0]})
        # if User_Id in dele:
        #     print("its already deleted")
        #     conn.commit()
        #     cur = conn.cursor()
        #     cur.execute('SELECT * FROM users where User_Id=%s', User_Id)
        #     res = cur.fetchall()
        #     print(db22,)
        #     return stored_password
        #     # res = jsonify('This is already deleted!')  # jsonifying the response
        #     #resp.status_code = 400  # giving status code 400 (False)
        #     #return resp

    #     """endtest"""
    #     if len(db22) != 0:  # checking condition if the user is not null
    #         cursor.execute("UPDATE  Users SET DELETE ='1'WHERE User_Id =%s", (User_Id,))  # qurey for deleting and it will
    #         # work only the value is not equal to null
    #         conn.commit()
    #         cur = conn.cursor()
    #         cur.execute('SELECT * FROM users where User_Id=%s', User_Id)
    #         res = cur.fetchall()
    #         l = []
    #         for i in res:
    #             for j in i:
    #                 l.append(j)
    #         # print(l[2])
    #         stored_password = l[11]
    #         print(stored_password,"ssssssssssssss")
    #         return stored_password
    #
    #         # resp = jsonify('User deleted successfully!')  # response is jsonifying
    #         #resp.status_code = 200  # giving status code as 200 (true)
    #         #return resp  # if the above condition works thengive the response as 200
    #     else:
    #         resp = jsonify({"message": "User doesn't exists!", "status": "400 Bad Request"})
    #         # res = jsonify("User not available with  id ", User_Id)  # if the user is null then this response works
    #         resp.status_code = 400  # error response
    #         return resp
    #
    # except Exception as e:
    #     print(e)
    # finally:
    #     cursor.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
