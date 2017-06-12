from Classes.dhl import dhl
from Classes.parcel import parcel
class ServiceManager(object):
		
	def call_service(self, company, service, paramlist):
		selected_class = globals()[company]
		instance = selected_class()
		method = getattr(instance, service)
		return method(paramlist)

# README
# This class is a factory class that will decide which concrete class to create an instance and which function to call
# It use function call_service to convert string from parameter to a class and a method