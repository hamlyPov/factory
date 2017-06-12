from ServiceManager import ServiceManager
import xml.etree.ElementTree as ET
import requests
import datetime
import re
import sys
#from flask import Flask
#from flask import request

#app = Flask(__name__)

myservice = ServiceManager()

# test dhl dropoff service
paramdhl = {}
paramdhl["pickup_date"] = "2017-05-26"
paramdhl["ready_by_time"] = "10:20"
paramdhl["close_time"] = "14:20"
myservice.call_service("dhl","pickup", paramdhl)

print ("\n")
# test parcel pickup service
paramparcel = {}
paramparcel['from'] = "France"
paramparcel['to'] = "Cambodia"
myservice.call_service("parcel", "pickup", paramparcel)


#========================= API GETWAY ================================
#@app.route("/<company>/<service>")
#def pickup(company, service):
#	return mys.0ervice.call_service(company, service, paramdhl)
#if __name0__=="__main__":
#	app.run()

