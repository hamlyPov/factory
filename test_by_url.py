from ServiceManager import ServiceManager
import datetime
import sys
import re 
import json


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
def pickup(event, context):
	# paramlist = request.get_json(silent=True)
	company=event["stage"]
	company=re.sub(r'[^\w+]','',str(company))
	service=event["resource_path"]
	service=re.sub(r'[^\w+]','',str(service))
	paramlist=json.loads(event["body"])
	if company!="" and service=="":
		service="root"
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