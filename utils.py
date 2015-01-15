#!/usr/bin/env python

import csv
import flickrapi
import json
import os
import time
import urllib


def connect_api(dbname, api_key, api_secret):
	if dbname == 'flickr':
		api = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
	return api

def write_metadata(metadata, filename, dbname='flickr', format='json'):
	timestr = time.strftime("_%Y%m%d-%H%M%S")
	if format == 'csv':
		counter = 1
		filename += timestr+'.csv'
		f = csv.writer(open(filename, 'w'))
		for d in metadata:
			f.writerow(['imagedb'],[dbname])
			for key, val in d.items():
				print '\nImage {}'.format(counter)
				f.writerow([key, val])
				counter += 1
	
	elif format == 'json':
		filename += timestr+'.json'
		f = open(filename, 'w')
		f.write(json.dumps(metadata))
		f.close()

	elif format == 'hdf':
		pass

	print 'Metada saved in {}'.format(filename)

def read_metadata(filename):

	if os.path.basename(filename).split('.')[1] == 'csv':
		pass
	elif os.path.basename(filename).split('.')[1] == 'json':
		json_data=open(filename)
		return json.load(json_data)

def get_source(metadata, format='original'):
	return metadata[format]['source'], metadata[format]['url']

def get_userid(metadata):
	return metadata['owner_id']

def get_image(url, filename):
	"""Given an URL save the image in filename. filename should specify the path.
	"""
	urllib.urlretrieve(url, filename)

def read_file(filename):
	"""Given a filename return the content of the file in a list."""
	
	if os.path.dirname(filename)=='':
		filename = os.path.join(os.getcwd(), filename)

	try:
		f = open(filename, 'r')
		lines = f.readlines()
		f.close()
		return lines
	except:
		print "Error: File {} does not exist.".format(filename)

