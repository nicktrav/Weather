#!/usr/bin/python
import urllib as u
import urllib2
import json
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
	url = 'http://www.bom.gov.au/fwo/IDW60901/IDW60901.94614.json'

	resp = urllib2.urlopen(url)
	data = json.loads(resp.read())

	latest_ob = data['observations']['data'][0]

	location = latest_ob['name']
	datetime_full = latest_ob['local_date_time_full']
	date = datetime_full[6:8] + '/' + datetime_full[4:6] + '/' + datetime_full[0:4] 
	time = datetime_full[8:10] + ':' + datetime_full[10:12]

	print '\nLatest observations for %s (as of %s local time):' % (location, time)
	print '\tAir temp: %.1fC' % latest_ob['air_temp']
	print '\tApparent temp: %.1fC' % latest_ob['apparent_t']
	print '\tWind speed: %d km/h' % latest_ob['wind_spd_kmh']
	print '\tWind direction: %s' % latest_ob['wind_dir']

	return	

def format_time_full(s):
	'''Format a BOM full time string to a time'''
	date = s[0:4] + '-' + s[4:6] + '-' + s[6:8] 
	time = s[8:10] + ':' + s[10:12]

	return (date, time)

def past():
	'''Weather observations for the past 24 hours'''
	# the lastest observations for Swanbourne
	url = 'http://www.bom.gov.au/fwo/IDW60901/IDW60901.94614.json'

	# Get the json
	resp = urllib2.urlopen(url)
	data = json.loads(resp.read())	

	# get all of the observations available
	location = data['observations']['header'][0]['name']
	observations = data['observations']['data']
	latest_time = format_time_full(observations[0]['local_date_time_full'])[1]

	print '\nLatest observations for %s (as of %s local time)' % (location, latest_time)
	template = "{0:^15}|{1:^10}|{2:^10}"
	print template.format("Date", "Time", "Air temp.")
	for obs in observations:
		(date, time) = format_time_full(obs['local_date_time_full'])
		air_temp = obs['air_temp']
		print template.format(*(date, time, air_temp))
	
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
	elif args.past:
		past()
	else:
		parser.print_help()
	
	return

if __name__ == '__main__':
	main()