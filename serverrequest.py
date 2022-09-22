#api to update server requests

from sre_constants import SUCCESS
from ssl import Purpose
from urllib import response
from flask import Flask, request, jsonify
from connect2db import *
import requests
from datetime import date
import time
date_today = date.today()
import datetime as datetime
date_today = date.today()
date_time = datetime.datetime.now()
d = datetime.datetime.strptime('2011-06-09', '%Y-%m-%d')
my_datetime_utc = date_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')


app = Flask(__name__)

@app.route('/update_u_comments' ,methods=['PUT']) 
def server_request(): 
    conn = connectDB()
    if request.method == 'PUT':
            _json = request.json
            ID = _json["ID"] 
            User_No = _json["ID"] 
            Creator = _json["Creator"]               
            Start_Date = _json["Start_Date"]     
            End_Date  = _json["End_Date"]         
            Manufacturer  = _json["Manufacturer"]         
            Number_Of_Servers = _json["Number_Of_Servers"]     
            Cpu_model = _json["Cpu_model"]        
            CPU_Sockets   =  _json["CPU_Sockets"]     
            DIMM_Size  = _json["DIMM_Size"]       
            DIMM_Capacity  =  _json["DIMM_Capacity"] 
            Storage_Vendor  =  _json["Storage_Vendor"]          
            Storage_Controller = _json["Storage_Controller"]     
            Storage_Capacity  = _json["Storage_Capacity"]   
            Network_Type  =  _json["Network_Type"]         
            Network_speed  = _json["Network_speed"]        
            Special_Switching_Needs =_json["Special_Switching_Needs"]
            User_Comments  = _json["User_Comments"]   
                   
 
            cursor= conn.cursor()

            data = (ID,User_No, Creator, Start_Date, End_Date,Manufacturer, Number_Of_Servers , Cpu_model, CPU_Sockets, DIMM_Size, DIMM_Capacity, Storage_Vendor, 
            Storage_Controller, Storage_Capacity , Network_Type, Network_speed, Special_Switching_Needs, User_Comments)
            cursor.execute("SELECT * FROM server_request  WHERE ID=%s", (ID,))
            print(data)
        
            #insert query
            cursor.execute("UPDATE server_request SET User_No=%s, Creator= %s, Start_Date= (%s), End_Date= (%s), Manufacturer= %s, Number_Of_Servers = %s , Cpu_model = %s, CPU_Sockets = %s, DIMM_Size = %s, DIMM_Capacity = %s, Storage_Vendor = %s, Storage_Controller = %s, Storage_Capacity = %s , Network_Type = %s, Network_speed = %s, Special_Switching_Needs = %s WHERE ID =%s", 
            (User_No,Creator,Start_Date,End_Date, Manufacturer, Number_Of_Servers , Cpu_model, CPU_Sockets, DIMM_Size, DIMM_Capacity, Storage_Vendor, 
            Storage_Controller , Storage_Capacity, Network_Type, Network_speed, Special_Switching_Needs, ID))

            #update query
            cursor.execute("UPDATE server_request SET User_Comments = array_prepend( %s, User_Comments) WHERE ID=%s", [str(User_Comments) + str(my_datetime_utc),ID])
    
           
            conn.commit()
            cursor.execute('select * from server_request where ID = %s',(ID,) ) 
            data = cursor.fetchall() 
            resp = jsonify({'message' : 'Server Request updated successfully !!', 'status' :'200 OK'})
            print(resp)
            resp.status_code = 200
            v = resp.status_code
            print(v)
            assert v == 200 , "code does'not match"
            return resp
            
        



if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)