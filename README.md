pymooney
========

This repository helds the python scripts to generate twotone, Mooney images. The main code is crmooney.py. 

You can 

(i) use search words that will be used to search images with these search words in online image databases and the Mooney images will be generated based on these images. (API key and secret are required). 

(ii) you can give a directory with images

(iii) you can give one image paath

The easiest way to use these scripts is to check the main-function in crmooney.py and write a wrapper funciton based on that.


Requirements
========

* flickrapi [Beej's Python Flickr API](http://stuvel.eu/media/flickrapi-docs/documentation/)

(You need a Flickr API key and secret if you want to make use of the image search. Check [here](https://www.flickr.com/services/api) for more information.)

* json

* scipy

* numpy

* skimage
* 

Citation
========

Please cite our Neuroimage paper if you use this package to create Mooney images.

[Fatma Imamoglu, Thorsten Kahnt, Christof Koch, John-Dylan Haynes, Changes in functional connectivity support conscious object recognition, NeuroImage, Volume 63, Issue 4, December 2012, Pages 1909–1917](http://www.sciencedirect.com/science/article/pii/S1053811912007860)
