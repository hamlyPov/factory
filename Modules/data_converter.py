class data_converter(object):

	# this function need to be tested
	def  json_converter(self, json_model, original_json):
		result = {}
		for key in json_model:
			result[key] = original_json[json_model[key]]
		return result
	#end json_converter

	# convert from xml(get from http) to json (standard response)
	def xml_converter(json_model, original_xml):
		result = {}
		for key in json_model:
			result[key] = original_xml.find(json_model[key]).text
		return result
	#end xml_converter