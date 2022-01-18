#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import json
import os
import time
import urllib

import flickrapi


def connect_api(dbname, api_key, api_secret):
    if dbname == "flickr":
        api = flickrapi.FlickrAPI(api_key, api_secret, format="parsed-json")
    return api


def write_metadata(metadata, filename, dbname="flickr", file_format="json"):
    timestr = time.strftime("_%Y%m%d-%H%M%S")
    if file_format == "csv":
        counter = 1
        filename += f"{timestr}.csv"
        with open(filename, "w") as file:
            writer = csv.writer(file)
            for data in metadata:
                writer.writerow(["imagedb"], [dbname])
                for key, val in data.items():
                    print(f"\nImage {counter}")
                    writer.writerow([key, val])
                    counter += 1

    elif file_format == "json":
        filename += timestr + ".json"
        with open(filename, "w") as file:
            file.write(json.dumps(metadata))

    elif file_format == "hdf":
        pass

    print(f"Metada saved in {filename}")


def read_metadata(filename):

    if os.path.basename(filename).split(".")[1] == "csv":
        pass
    elif os.path.basename(filename).split(".")[1] == "json":
        with open(filename, "r", encoding="utf8") as file:
            return json.load(file)
    return None


def get_source(metadata, format_="original"):
    return metadata[format_]["source"], metadata[format_]["url"]


def get_userid(metadata):
    return metadata["owner_id"]


def get_image(url, filename):
    """Given an URL save the image in filename.

    filename should specify the path.
    """
    urllib.request.urlretrieve(url, filename)


def read_file(filename):
    """Given a filename return the content of the file in a list."""

    if os.path.dirname(filename) == "":
        filename = os.path.join(os.getcwd(), filename)

    try:
        with open(filename, "r", encoding="utf8") as file:
            lines = file.readlines()
        return lines
    except IOError:
        print(f"Error: File {filename} does not exist.")

    return None
