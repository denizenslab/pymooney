#!/usr/bin/env python

import flickrapi
import os

def get_license_info(flickr):
    licenses = flickr.photos.licenses.getInfo()['licenses']['license']
    print '\n############# Flickr license information #############\n'
    for license in sorted(licenses):
        print 'ID: {0}, Name: {1}, url: {2}'.format(license['id'], license['name'], license['url'])
    print '\n######################################################\n'

def get_metadata(flickr, photo):
    """ Given a flickrapi object and a photo flickrapi object return the metadata. """
    photo_meta = dict()
    photo_meta['photo_id'] = photo['id']
    
    info = flickr.photos.getInfo(photo_id=photo['id'])
    photo_meta['owner'] = info['photo']['owner']['username']
    photo_meta['owner_id'] = info['photo']['owner']['nsid']
    photo_meta['secret'] = info['photo']['secret']
    photo_meta['license'] = info['photo']['license']

    if info['photo']['usage']['candownload'] == 1:

        ## Get the original sized image url and size
        photo_meta['original'] = [{'url':p_size['url'].encode('ascii', 'ignore'), 'source':p_size['source'].encode('ascii', 'ignore'), 'height':p_size['height'], 'width':p_size['width']} 
                                    for p_size in flickr.photos.getSizes(photo_id=photo['id'])['sizes']['size'] if p_size['label']=='Original' ][0]

        ## Get the large squared image url and size
        photo_meta['large_square'] = [{'url':p_size['url'].encode('ascii', 'ignore'), 'source':p_size['source'].encode('ascii', 'ignore'), 'height':p_size['height'], 'width':p_size['width']}
                                    for p_size in flickr.photos.getSizes(photo_id=photo['id'])['sizes']['size'] if p_size['label']=='Large Square' ][0]
    return photo_meta

def get_photo_id(photo):
    """ Given a photo flickrapi object return the flickr photo id. """
    return photo['id']
