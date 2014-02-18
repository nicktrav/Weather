import urllib as u
import xml.etree.ElementTree as ET
import dateutil.parser
import datetime
import sys, os
import argparse

def getAttribute(root, attrib):
	res = root.find("./*[@type='"+attrib+"']")

	if res != None:
		return res.text
	else:
		return None

def forecast():
	url = 'ftp://ftp2.bom.gov.au/anon/gen/fwo/IDW14199.xml'
	xml_feed = u.urlopen(url)

	tree = ET.parse(xml_feed)
	root = tree.getroot()

	location = root.findall("./forecast/*[@aac='WA_PT060']/*")

	forecasts = location[1:] # index 0 is the current, so ignore

	for forecast in forecasts:
		forecast_date = dateutil.parser.parse(forecast.attrib['start-time-local'])
		forecast_temp_max = getAttribute(forecast, 'air_temperature_maximum')
		forecast_temp_min =  getAttribute(forecast, 'air_temperature_minimum')
		forecast_precis = getAttribute(forecast, 'precis')

		print forecast_date.strftime("%A, %d. %B")
		print '\tForecast maximum: %s' % forecast_temp_max
		print '\tForecast minimum: %s' % forecast_temp_min
		print '\tPrecis: %s' % forecast_precis

	return

def current():
	url = 'ftp://ftp2.bom.gov.au/anon/gen/fwo/IDW14199.xml'
	xml_feed = u.urlopen(url)

	tree = ET.parse(xml_feed)
	root = tree.getroot()

	location = root.findall("./forecast/*[@aac='WA_PT060']/*")
	current_forecast = location[0] # the first item is the current forecast period

	forecast_items = {'Outlook': None, 'Maximum': None, 'Minimum': None}

	getAttribute(current_forecast, 'air_temperature_minimum')

	forecast_items['Minimum'] = getAttribute(current_forecast, 'air_temperature_minimum')
	forecast_items['Maximum'] = getAttribute(current_forecast, 'air_temperature_maximum')
	forecast_items['Outlook'] = getAttribute(current_forecast, 'precis')

	if forecast_items['Minimum'] != None: print 'Minimum: %f' % forecast_items['Minimum']
	if forecast_items['Maximum'] != None: print 'Maximum: %f' % forecast_items['Maximum']
	if forecast_items['Outlook'] != None: print 'Outlook: %s' % forecast_items['Outlook']

	return	

def main():

	parser = argparse.ArgumentParser()
	parser.add_argument("-f", "--forecast", help="7 day forecast", action="store_true")
	parser.add_argument("-c", "--current", help="Current temperature", action="store_true")
	parser.add_argument("-p", "--past", help="Temperatures frorm the last 24 hours", action="store_true")
	args = parser.parse_args()

	if args.forecast:
		forecast()
	elif args.current:
		current()
	else:
		parser.print_help()
	return

if __name__ == '__main__':
	main()