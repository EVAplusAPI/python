# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 08:08:55 2020

@author: dietiker
"""
#pip install requests
#https://www.geeksforgeeks.org/get-post-requests-using-python/

import requests 
import json 

tenantkey="dev" 
username="apiusername"
password="****"

CREDENTIALS = { "username": username, "password": password}  

def apiRequest(CREDENTIALS,tenantkey,DATAURL,PARAM=""):
    rooturl = "https://"+tenantkey+".evaplus.com/EvaCloudAPI/"
    LOGINURL = rooturl+"login"
    LOGOUTURL = rooturl+"logout"
    data=""
    response = requests.post(url = LOGINURL, data = json.dumps(CREDENTIALS)) 
    print(response)#200 is ok
    if response.status_code == 200:
        print("successfully logged in")
        obj = json.loads(response.text)
        token=obj['token']           
        auth={ "Authorization" : token } 
        
        if PARAM == "": 
            response = requests.get(url = DATAURL, headers = auth) 
        else:
            response = requests.post(url = DATAURL, headers = auth, data = json.dumps(PARAM))           
            
        if response.status_code == 200:            
            data = json.loads(response.text)            
        else:             
            data = response.status_code            
        
        response = requests.post(url = LOGOUTURL, headers = auth)       
            
        if response.status_code == 200:            
            logoutresponse = json.loads(response.text)
            print(logoutresponse)
        else: 
            print(response.status_code)
            print("logout failed")
    else:             
        data = response.status_code
        
    return data

rooturl="https://"+tenantkey+".evaplus.com/EvaCloudAPI/"
FLEETURL = rooturl+"getVehicleFleet"
EVENTTYPELURL = rooturl+"getEventNameList"
EVENTURL=rooturl+"getEvents"

#getting all fleets and vehicles
vehiclelist=apiRequest(CREDENTIALS,tenantkey,FLEETURL)
print(vehiclelist)
for entry in vehiclelist:
    print (entry['fleet'])

#getting all WSP events from one vehicle
PARAM = { "vehicleId" : "357324_A",
	  "startTime": "202003020000",
	  "endTime": "202003020600",
	  "events": ["WSP_event"],
	  "page": "0"}
events=apiRequest(CREDENTIALS,tenantkey,EVENTURL,PARAM)
print(events)

print('done')    