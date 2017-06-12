from ServiceManager import ServiceManager
# from BuiltInService
import xml.etree.ElementTree as ET
import requests
import datetime
# from BuiltInService import re
# from BuiltInService import *
import sys
# from flask import Flask
# from flask import request

# app = Flask(__name__)

myservice = ServiceManager()

# test dhl dropoff service
# paramdhl = {}
# paramdhl["pickup_date"] = "2017-05-26"
# paramdhl["ready_by_time"] = "10:20"
# paramdhl["close_time"] = "14:20"
# myservice.call_service("dhl","pickup", paramdhl)

print ("\n")
# test parcel pickup service
# paramparcel = {}
# paramparcel['from'] = "France"
# paramparcel['to'] = "Cambodia"
# myservice.call_service("parcel", "pickup", paramparcel)


#========================= API GETWAY ================================
# @app.route("/<company>/<service>", methods = ["POST"])
def pickup(company, service):
	# paramlist = request.get_json(silent=True)
	paramlist={
	  "requestor": {
	    "name": "Rikhil",
	    "phone": "23162",
	    "company": "Saurabh"
	  },
	  "place": {
	    "line1": "123 Test Ave",
	    "line2": "Test Bus Park",
	    "package_location": "Reception",
	    "city": "PARIS",
	    "post_code": "75018",
	    "country_code": "FR"
	  },
	  "pick_up": {
	    "pickup_date": "2017-06-13",
	    "slot_id": "string",
	    "ready_by_time": "10:20",
	    "close_time": "23:20",
	    "number_of_pieces": 0,
	    "special_instructions": "1 palett of 200 kgs - Vehicule avec hayon"
	  },
	  "shipment_details": {
	    "number_of_pieces": 1,
	    "weight": 200
	  }
	}
	company="dhl"
	service="pickup"
	return myservice.call_service(company, service, paramlist)
if __name__=="__main__":
	app.run()

#============ README ==========
# """
# 	Please use postman or other api testing tool to test with the following information
# 	1. URL: http://localhost:5000/company/service (ex. http://localhost:5000/dhl/pickup, http://localhost:5000/parcel/dropoff)
# 	2. requestType: post
# 	3A. request object format for dhl:
# 		{
# 			"pickup_date": "2017-05-26",
# 			"ready_by_time":"12:20",
# 			"close_time":"16:20"
# 		}

# 	3B. request object format for parcel: 
# 		{
# 			"from": "Australia",
# 			"to":"France"
# 		}
	
# """