from Classes.AbstractService import Service
from BuiltInService import requests
# from BuiltInService 
import re
import time
import datetime
# from BuiltInService 
import xml.etree.ElementTree as ET
from Modules.data_converter import data_converter as converter
from Modules.network import networking as netw
# from BuiltInService
import json
import os
from random import randrange

import base64
import boto
from boto.s3.key import Key
from boto.s3.connection import S3Connection


DHL_URL = "https://xmlpitest-ea.dhl.com/XMLShippingServlet"
# netw = networking()
class dhl(Service):	
	
	def root(self,paramlist):
		true=True
		data={
			"/":{
				"get":true
			},
			"type":{
				"get":true
			},
			"pickup/slots":{
				"get":true
			},
			"price":{
				"get":true
			},
			"status":{
				"get":true
			}
		}
		return data
		

	def pickup(self, paramlist):
			
		# STEP 1: Load "request object parameter" from assets (can be xml or json) 
		tree = ET.parse('Assets/dhl/requests/003_Pickup.txt')
		root = tree.getroot()

		# STEP 2: set value to object property
		datenow=str(datetime.datetime.now())
		datenow=re.sub(r'\..*','',datenow)
		messageReference=str(randrange(0,10000000000000000000000000000000))
		messageTime=str(datenow)+"T11:28:56.000-08:00"
		root.find("Request/ServiceHeader/MessageTime").text = messageTime
		root.find("Request/ServiceHeader/MessageReference").text = messageReference

		root.find("Request/ServiceHeader/SiteID").text = os.environ["DHL_USERID"]
		root.find("Request/ServiceHeader/Password").text = os.environ["DHL_PWD"]

		root.find("Pickup/PickupDate").text = paramlist["pickup"]["pickup_date"]   #paramlist["pickup_date"] # "2017-05-26"
		root.find("Pickup/ReadyByTime").text = paramlist["pickup"]["ready_by_time"] #paramlist["ready_by_time"] # "10:20"
		root.find("Pickup/CloseTime").text = paramlist["pickup"]["close_time"]  #paramlist["close_time"] # "14:20"
		
		root.find("Place/CompanyName").text = paramlist["requestor"]["company"]
		root.find("Place/Address1").text = paramlist["place"]["line1"]
		root.find("Place/Address2").text = paramlist["place"]["line2"] 
		root.find("Place/PackageLocation").text = paramlist["place"]["package_location"] 
		root.find("Place/City").text = paramlist["place"]["city"] 
		root.find("Place/CountryCode").text = paramlist["place"]["country_code"] 
		root.find("Place/PostalCode").text = paramlist["place"]["post_code"] 

		root.find("PickupContact/PersonName").text = paramlist["requestor"]["name"] 
		root.find("PickupContact/Phone").text = paramlist["requestor"]["phone"] 

		root.find("ShipmentDetails/NumberOfPieces").text = str(paramlist["shipment_details"]["number_of_pieces"])
		root.find("ShipmentDetails/Weight").text = str(paramlist["shipment_details"]["weight"])

		# more variable can be set to xml here ... 

		xmlresult = ET.tostring(root, encoding='ascii', method='xml')

		# STEP 3: 	REQUEST DATA
		# the 2 following lines are called when accessing real data from http
		xmlresponse = netw.sendRequest(DHL_URL, xmlresult, "post", "xml", "xml")
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
			# final_result = converter.xml_converter(json_model, xmlroot)
			final_result=converter.xml_converter_Pickup(json_model,xmlroot,paramlist)
			print ("Pickup Info from DHL: \n"+str(final_result))
			return  final_result
		except:
			return "Cannot get data from the URL"+str(xmlresponse)

	def status(self,paramlist):
		print ("type function")
		date = datetime.datetime.now()
		datenow=re.sub(r'\s.*','',str(date))
		tree = ET.parse('Assets/dhl/requests/003_Pickup.txt')
		root = tree.getroot()
		root.find("Pickup/PickupDate").text = datenow
		# root.find("Request/ServiceHeader/SiteID").text = os.environ["DHL_USERID"]
		# root.find("Request/ServiceHeader/Password").text = os.environ["DHL_PWD"]
		start=time.time()
		available=True
		response_time=0
		xmlresult = ET.tostring(root, encoding='ascii', method='xml')
		try:
			xmlresponse = netw.sendRequest(DHL_URL, xmlresult, "post", "xml", "xml")
			xmlroot = ET.fromstring(xmlresponse)
		except:
			available=False
		response_time=-1

		if response_time==0:
			response_time=time.time()-start

		timeout=False

		if response_time>30:
			timeout=True

		result = {
		    "available": available,
		    "response_time": response_time,
		    "timeout": timeout,
		    "limit": 30000
		}
		return result


	def pickupslots(self, paramlist):
		print ("pickupslots from DHL")
		date = datetime.datetime.now()
		alldays=[]
		for l in range(7):
			date += datetime.timedelta(days=1)
			if date.isoweekday()==6:
				date += datetime.timedelta(days=2)
				print ("saturday +2: "+str(date))
			elif date.isoweekday()==7:
				date += datetime.timedelta(days=1)
				print ("sunday +1: "+str(date))
			else:
				print ("no check")
			newdate=re.sub(r'\s.*',' ',str(date))
			fullstartdate1=str(newdate)+" 10:00:00:000Z"
			fullstartdate2=str(newdate)+" 12:00:00:000Z"
			fullstartdate3=str(newdate)+" 14:00:00:000Z"
			fullstartdate4=str(newdate)+" 16:00:00:000Z"
			fullstartdate5=str(newdate)+" 18:00:00:000Z"
			data={
		        "date": str(date),
		        "slots": [
			        {
						"start_time": fullstartdate1,
				        "duration": "120",
				        "availability": -1
					},
					{
						"start_time": fullstartdate2,
				        "duration": "120",
				        "availability": -1
					},
					{
						"start_time": fullstartdate3,
				        "duration": "120",
				        "availability": -1
					},
					{
						"start_time": fullstartdate4,
				        "duration": "120",
				        "availability": -1
					},
					{
						"start_time": fullstartdate5,
				        "duration": "120",
				        "availability": -1
					}
				]
		    }

			alldays.append(data)
		return alldays

	def label(self,paramlist):
		print ("label function")
		tree = ET.parse('Assets/dhl/requests/002_Shipment_FR_BE.txt')
		root = tree.getroot()

		date = datetime.datetime.now()
		datenow=re.sub(r'\s.*','',str(date))

		s3key1=os.environ["S3_KEY1"]
		s3key2=os.environ["S3_KEY2"]

		origin_country=str(paramlist["origin"]["country"])
		if origin_country=="FR":
			shipperAccountNumber= os.environ["SHIPPER_ACCOUNT_NUMBER_EXPORT"]
		else:
			shipperAccountNumber=os.environ["SHIPPER_ACCOUNT_NUMBER_IMPORT"]

		messageTime=str(datenow)+"T11:28:56.000-08:00"
		messageReference=str(randrange(0,10000000000000000000000000000000))
		if "shipment_date" not in paramlist:
			return "shipmentdate is missing..."
		shipmentdate=str(paramlist["shipment_date"])
		if shipmentdate=="":
			return "shipmentdate is missing..."

		if "shipment_id" not in paramlist["destination"]:
			return "destination_shipmentId is missing..."
		destination_shipmentId=str(paramlist["destination"]["shipment_id"])
		if destination_shipmentId=="":
			return "destination_shipmentId is missing..."

		if "company" not in paramlist["destination"]:
			return "CompanyName destination  is missing..."

		destination_company=str(paramlist["destination"]["company"])
		if destination_company=="":
			return "CompanyName destination is missing..."
		if "line1" not in paramlist["destination"]:
			return "One of the address in destination must be completed..."
		if "line2" not in paramlist["destination"]:
			return "one of the address in destination must be completed.."

		destination_line1=str(paramlist["destination"]["line1"])
		destination_line2=str(paramlist["destination"]["line2"])
		destination_line1=destination_line1+" "+destination_line2
		if "city" not in paramlist["destination"]:
			destination_city=""
		else:
			destination_city=str(paramlist["destination"]["city"])

		if "state" not in paramlist["destination"]:
			destination_state=""
		else:
			destination_state=str(paramlist["destination"]["state"])

		if "zipcode" not in paramlist["destination"]:
			destination_zipcode=""
		else:
			destination_zipcode=str(paramlist["destination"]["zipcode"])

		if "country_code" not in paramlist["destination"]:
			return "destination_countryCode  is missing..."
		destination_countryCode=str(paramlist["destination"]["country_code"])
		if destination_countryCode=="":
			return "destination_countryCode is mandatory"
		if "country" not in paramlist["destination"]:
			return "destination_country_name is missing"

		destination_country=str(paramlist["destination"]["country"])
		if destination_country=="":
			return "destination_country_name is mandatory"
		if "name" not in paramlist["destination"]:
			destination_name=""
		else:
			destination_name=str(paramlist["destination"]["name"])

		if "phone" not in paramlist["destination"]:
			destination_phone=""
		else:
			destination_phone=str(paramlist["destination"]["phone"])
		# if destination_phone=="":
		# 	return "destination_phone is mandatory"

		if "first_name" not in paramlist["destination"]:
			return "destination_firstname is missing ...."
		destination_firstname=str(paramlist["destination"]["first_name"])

		if "last_name" not in paramlist["destination"]:
			return "destination_lastname is missing .."
		destination_lastname=str(paramlist["destination"]["last_name"])

		if destination_firstname=="":
			return "destination_firstname cannot be empty."

		if destination_lastname=="":
			return "destination_lastname cannot be empty"

		destination_fullname=str(destination_firstname)+" "+str(destination_lastname)

		if "email" not in paramlist["destination"]:
			destination_email=""
		else:
			destination_email=str(paramlist["destination"]["email"])

		if "weight_in_grams" not in paramlist["parcel"]:
			parcel_weight_in_grams="0.0"
		else:
			parcel_weight_in_grams=str(paramlist["parcel"]["weight_in_grams"])
			parcel_weight_in_grams=str(float(parcel_weight_in_grams)/1000)
			if parcel_weight_in_grams <= "0":
				parcel_weight_in_grams="0.0"

		if "width_in_cm" not in paramlist["parcel"]:
			parcel_width_in_cm=""
		else:
			parcel_width_in_cm=str(paramlist["parcel"]["width_in_cm"])

		# if parcel_width_in_cm=="0":
		# 	return "width_in_cm must be more than 0"
		if "height_in_cm" not in paramlist["parcel"]:
			parcel_height_in_cm=""
		else:
			parcel_height_in_cm=str(paramlist["parcel"]["height_in_cm"])


		if "length_in_cm" not in paramlist["parcel"]:
			parcel_length_in_cm=""
		else:
			parcel_length_in_cm=str(paramlist["parcel"]["length_in_cm"])

		if "contents" not in paramlist:
			contents=""
		else:
			contents= str(paramlist["contents"])

		if "first_name" not in paramlist["origin"]:
			origin_firstname=""
		else:
			origin_firstname=str(paramlist["origin"]["first_name"])
		
		if "last_name" not in paramlist["origin"]:
			last_name=""
		else:
			origin_lastname=str(paramlist["origin"]["last_name"])
		
		if "company" not in paramlist["origin"]:
			origin_company=""
		else:
			origin_company=str(paramlist["origin"]["company"])
		
		if "city" not in paramlist["origin"]:
			return "origin_city is missing.."
		origin_city=str(paramlist["origin"]["city"])

		if origin_city=="":
			return "origin_city cannot be empty"
		if "line1" not in paramlist["origin"]:
			return "origin_line1 is missing"
		origin_line1=str(paramlist["origin"]["line1"])
		if origin_line1 =="":
			return "origin_line1 cannot be empty"
		if "line2" not in paramlist["origin"]:
			origin_line2=""
		else:
			origin_line2=str(paramlist["origin"]["line2"])+""
		
		origin_line1=origin_line1+" "+origin_line2

		if "country" not in paramlist["origin"]:
			return "origin_country is missing"

		if origin_country=="":
			return "origin_country cannot be empty"

		if "zipcode" not in paramlist["origin"]:
			origin_zipcode=""
		else:
			origin_zipcode=str(paramlist["origin"]["zipcode"])+""
		

		if "country_code" not in paramlist["origin"]:
			return "origin_countrycode is missing..."

		origin_countrycode=str(paramlist["origin"]["country_code"])
		if origin_countrycode=="":
			return "origin_countrycode cannot be empty"

		if "name" not in paramlist["origin"]:
			return "origin_name is missing.."
		origin_name=str(paramlist["origin"]["name"])
		if origin_name=="":
			return "origin_name cannot be empty"
		if "phone" not in paramlist["origin"]:
			origin_phone=""
		else:
			origin_phone=str(paramlist["origin"]["phone"])
		
		if "email" not in paramlist["origin"]:
			return "origin email is missing .."
		origin_email=str(paramlist["origin"]["email"])
		
		if "state" not in paramlist["origin"]:
			origin_state=""
		else:
			origin_state=str(paramlist["origin"]["state"])
		
		if "place_description" not in paramlist["origin"]:
			origin_packagelocation=""
		else:
			origin_packagelocation=str(paramlist["origin"]["place_description"])

		root.find("Request/ServiceHeader/MessageTime").text = messageTime
		root.find("Request/ServiceHeader/MessageReference").text = messageReference

		root.find("Request/ServiceHeader/SiteID").text = os.environ["DHL_USERID"]
		root.find("Request/ServiceHeader/Password").text = os.environ["DHL_PWD"]

		root.find("Billing/ShipperAccountNumber").text = shipperAccountNumber
		root.find("Billing/BillingAccountNumber").text = shipperAccountNumber
		root.find("Consignee/CompanyName").text = destination_company
		root.find("Consignee/AddressLine").text = destination_line1
		root.find("Consignee/City").text = destination_city
		root.find("Consignee/Division").text = destination_state
		root.find("Consignee/PostalCode").text = destination_zipcode
		root.find("Consignee/CountryCode").text = destination_countryCode
		root.find("Consignee/CountryName").text = destination_country
		root.find("Consignee/Contact/PersonName").text = destination_fullname
		root.find("Consignee/Contact/PhoneNumber").text = destination_phone
		root.find("Consignee/Contact/Email").text = destination_email
		root.find("Consignee/Contact/MobilePhoneNumber").text = destination_phone

		root.find("Commodity/CommodityCode").text = destination_shipmentId
		# root.find("ShipmentDetails/NumberOfPieces").text = destination_shipmentId
		root.find("ShipmentDetails/Pieces/Piece/Weight").text = parcel_weight_in_grams
		root.find("ShipmentDetails/Pieces/Piece/Width").text = parcel_width_in_cm
		root.find("ShipmentDetails/Pieces/Piece/Height").text = parcel_height_in_cm
		root.find("ShipmentDetails/Pieces/Piece/Depth").text = parcel_length_in_cm
		root.find("ShipmentDetails/Weight").text = parcel_weight_in_grams
		root.find("ShipmentDetails/Date").text = shipmentdate
		root.find("ShipmentDetails/Contents").text = contents

		root.find("Shipper/ShipperID").text = shipperAccountNumber
		root.find("Shipper/CompanyName").text = origin_company
		root.find("Shipper/AddressLine").text = origin_line1
		# root.find("Shipper/AddressLine").text = origin_line2
		root.find("Shipper/City").text = origin_city
		root.find("Shipper/PostalCode").text = origin_zipcode
		root.find("Shipper/CountryCode").text = origin_countrycode
		root.find("Shipper/CountryName").text = origin_country
		root.find("Shipper/Contact/PersonName").text = origin_firstname+" "+origin_lastname
		root.find("Shipper/Contact/PhoneNumber").text = origin_phone
		root.find("Shipper/Contact/Email").text = origin_email

		root.find("Place/CompanyName").text = origin_company
		root.find("Place/AddressLine").text = origin_line1
		root.find("Place/City").text = origin_city
		root.find("Place/CountryCode").text = origin_countrycode
		root.find("Place/Division").text = origin_state
		root.find("Place/PostalCode").text = origin_zipcode
		root.find("Place/PackageLocation").text = origin_packagelocation

		c = boto.connect_s3(s3key1, s3key2)
		b = c.get_bucket("srbstickers", validate=False)

		xmlresult = ET.tostring(root, encoding='ascii', method='xml')
		xmlresponse = netw.sendRequest(DHL_URL, xmlresult, "post", "xml", "xml")
		xmlroot = ET.fromstring(xmlresponse)

		for child in xmlroot.findall('LabelImage'):
			pdf=child.find('OutputFormat').text+'.pdf'
			img_data=child.find('OutputImage').text
			name_file=str(time.time())+".pdf"
			k = Key(b)
			k.key = name_file
			k.contentType="application/pdf"
			k.ContentDisposition="inline"
			# k.set_contents_from_string(img_data.decode('base64'))
			k.set_contents_from_string(base64.b64decode(img_data.encode('ascii')))
			link_pdf="https://s3-us-west-2.amazonaws.com/srbstickers/"+name_file

		
		shipmentId="0"
		for getchild in xmlroot.findall('AirwayBillNumber'):
			if len(getchild)<0:
				shipmentId= ''
			else:
				shipmentId=getchild.text

		if shipmentId=="0":
			return xmlresponse
		data={
		  "origin": paramlist["origin"],
		  "destination": paramlist["destination"],
		  "parcel": paramlist["parcel"],
		  "shipment_id": shipmentId,
		  "label_url": link_pdf
		}
		return data










	def price(self,paramlist):
		print ("price function")
		date = datetime.datetime.now()
		datenow=re.sub(r'\s.*','',str(date))
		tree = ET.parse('Assets/dhl/requests/003_Pickup.txt')
		root = tree.getroot()

		root.find("Request/ServiceHeader/SiteID").text = os.environ["DHL_USERID"]
		root.find("Request/ServiceHeader/Password").text = os.environ["DHL_PWD"]
		root.find("Pickup/PickupDate").text = datenow

		xmlresult = ET.tostring(root, encoding='ascii', method='xml')
		xmlresponse = netw.sendRequest(DHL_URL, xmlresult, "post", "xml", "xml")
		xmlroot = ET.fromstring(xmlresponse)
		try:
			shipment_id=xmlroot.find("ConfirmationNumber").text
		except:
			return xmlresponse
		currency="$"
		data={
			"destination":paramlist["destination"],
			"origin":paramlist["origin"],
			"parcel":paramlist["parcel"],
			"shipment_id": shipment_id,
			"price":0,
			"currency":currency
	    }
		return data


	def type(self,paramlist):
		print ("status function")
		true=True
		data={
			"type": "postal",
			"postal": true,
			"pickup": true,
			"dropoff": true,
			"linehaul": true
		}
		return data



# ============== README ================
# The processes of each function in this class are:
# 1. Load "request object parameter" from assets (can be xml or json)
# 2. set value to object parameter 
# 3. get "response object" from http with request parameter (just set in step 2)
# 4A. Load "json_model"from assets
# 4B. Note: "json_model" is a standard response object. Each service should have one standard json response object
# 5. convert "response_object" to "json_model" and return result