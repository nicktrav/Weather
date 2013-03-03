import urllib as u
import xml.etree.ElementTree as ET
import dateutil.parser
import datetime
import sys, os
import argparse

def forecast():
	url = 'ftp://ftp2.bom.gov.au/anon/gen/fwo/IDW14199.xml'
	xml_feed = u.urlopen(url)

	tree = ET.parse(xml_feed)
	root = tree.getroot()

	fremantle = root.findall("./forecast/*[@aac='WA_PT028']/*")

	forecasts = fremantle[1:]

	for forecast in forecasts:
		forecast_date = dateutil.parser.parse(forecast.attrib['start-time-local'])
		forecast_temp_max = forecast.find("./*[@type='air_temperature_maximum']").text
		forecast_temp_min = forecast.find("./*[@type='air_temperature_minimum']").text
		forecast_precis = forecast.find("./*[@type='precis']").text

		print forecast_date.strftime("%A, %d. %B")
		print '\tForecast maximum: %s' % forecast_temp_max
		print '\tForecast minimum: %s' % forecast_temp_min
		print '\tPrecis: %s' % forecast_precis

	return

def main():


	parser = argparse.ArgumentParser()
	parser.add_argument("-f", "--forecast", help="7 day forecast", action="store_true")
	parser.add_argument("-c", "--current", help="Current temperature", action="store_true")
	parser.add_argument("-p", "--past", help="Temperatures frorm the last 24 hours", action="store_true")
	args = parser.parse_args()

	if args.forecast:
		forecast()

	return

if __name__ == '__main__':
	main()