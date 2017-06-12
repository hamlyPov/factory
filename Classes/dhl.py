from Classes.AbstractService import Service
import requests
import re
# from BuiltInService 
import xml.etree.ElementTree as ET
from Modules.data_converter import data_converter as converter
from Modules.network import networking as net
import json
DHL_URL = "https://xmlpitest-ea.dhl.com/XMLShippingServlet"

class dhl(Service):	
	
	def pickup(self, paramlist):
			
			# STEP 1: Load "request object parameter" from assets (can be xml or json) 
			tree = ET.parse('Assets/dhl/requests/003_Pickup.txt')
			root = tree.getroot()

			# STEP 2: set value to object property
			root.find("Pickup/PickupDate").text = paramlist["pick_up"]["pickup_date"]   #paramlist["pickup_date"] # "2017-05-26"
			root.find("Pickup/ReadyByTime").text = paramlist["pick_up"]["ready_by_time"]#paramlist["ready_by_time"] # "10:20"
			root.find("Pickup/CloseTime").text = paramlist["pick_up"]["close_time"]#paramlist["close_time"] # "14:20"
			# more variable can be set to xml here ... 

			xmlresult = ET.tostring(root, encoding='ascii', method='xml')

			# STEP 3: 	REQUEST DATA
			# the 2 following lines are called when accessing real data from http
			xmlresponse = net.sendRequest(DHL_URL, xmlresult, "post", "xml", "xml")
			xmlroot = ET.fromstring(xmlresponse)

			""" The following lines are for testing purpose only (the json data is in local, not a real data from http)
			 Sometimes the http response an error object. To test with error object use file "ObjectName_Fail.xml"
			 located at the same level with "ObjectName_Success.xml"
			"""
			#xmlresponse = ET.parse("Assets/dhl/test_response/003_Pickup_Success.xml")
			#xmlroot = xmlresponse.getroot()

			# Prevent Error
			try:
			# STEP 4: Load "json_model"from assets
				with open("Assets/dhl/json_response_model/003_Pickup.json") as data_file:
					json_model = json.load(data_file)

				# STEP 5. convert "response_object" to "json_model" and return result ##NEED PARAMSLIST
				final_result = converter.xml_converter(json_model, xmlroot)
				print ("Pickup Info from DHL: \n"+str(final_result))
				return  str(final_result)
			except:
				return "Cannot get data from the URL"

	def dropoff(self, paramlist):
		print ("Dropoff from DHL. This function needs implementation.")
		return "Welcome DHL pickup"

	# more function can be implemeted here ...



# ============== README ================
# The processes of each function in this class are:
# 1. Load "request object parameter" from assets (can be xml or json)
# 2. set value to object parameter 
# 3. get "response object" from http with request parameter (just set in step 2)
# 4A. Load "json_model"from assets
# 4B. Note: "json_model" is a standard response object. Each service should have one standard json response object
# 5. convert "response_object" to "json_model" and return result