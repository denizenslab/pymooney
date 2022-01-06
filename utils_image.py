#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import numpy as np
from matplotlib.pyplot import imread
from matplotlib.pyplot import imsave
from PIL import Image
from scipy import ndimage
from skimage.filters import rank
from skimage.filters import threshold_otsu
from skimage.morphology import disk


def load_imgs(path):
    """Given a path load image(s). The input path can either be (i) a directory
    in which case all the JPG-images will be loaded into a dictionary, or (ii)
    an image file.

    Returns:
    imgs: A dictionary of of n-dim images. Keys are the original filenames
    """
    ## Get filenames
    filenames = []
    if os.path.isdir(path):
        print(f"Images in {path} will be loaded")
        for file in os.listdir(path):
            if file.endswith(".jpg"):
                filenames.append(os.path.basename(file))
        imagepath = path
    else:
        filenames.append(os.path.basename(path))
        imagepath = os.path.dirname(path)
    print(f"{len(filenames)} images found in {path}")

    ## Load images
    imgs = {}
    for file in filenames:
        print(f"\nImage: {file}")
        imgs[file] = imread(os.path.join(imagepath, file))

    return imgs


def save_img(img, filename):
    """Given a numpy array image save image under filename."""

    if os.path.dirname(filename) == "":
        path = os.getcwd()
    else:
        path = os.path.dirname(filename)

    if not os.path.exists(path):
        os.makedirs(path)

    filename = os.path.join(path, filename)
    imsave(filename, img)


def rename_imgs(path):
    """Given a path rename image(s). The input path can either be (i) a
    directory in which case all the JPG-images will be loaded into a
    dictionary, or (ii) an image file.

    The filename, the original file id and other metadata will be stored
    into a text file in the same directory.
    """
    pass


def resize_img(img, size=(400, 400), resample=Image.BILINEAR):
    return np.asarray(Image.fromarray(np.uint8(img)).resize(size, resample))


def rgb2gray(img):
    """Given an RGB image return the gray scale image.

    Based on http://en.wikipedia.org/wiki/Grayscale#Converting_color_to_grayscale
    img = 0.299 R + 0.587 G + 0.114 B
    """
    print("Convert RGB image to gray scale.")
    return np.uint8(np.dot(img[..., :3], [0.299, 0.587, 0.114]))


def gauss_filter(img, sigma=4, mode="nearest"):
    print(f"Smooth image using a Gaussian kernel sigma {sigma}")
    return ndimage.filters.gaussian_filter(img, sigma=sigma, mode=mode)


def median_filter(img, size=4):
    print(f"Smooth image using a median filter size {size}")
    return ndimage.filters.median_filter(img, size)


def threshold_img(img, method="global_otsu", radius=50):
    """ Given a gray scale image return a thresholded binary image using Otsu's thresholding method.
    img: A gray scale numpy array.
    method:
      - 'global_otsu' computes a global threshold  value for the whole image and uses this to binarize the
      input image. (default)
      - 'local_otsu' computes a local threshols value for each pixel (threshold is computed within a neighborhood of a radius).

    radius: The 2D neighborhood to compute local thresholds in local_otsu method

    Returns:

    img_binary: A binary image (same size as input img).
    threshold: Threshold value used to binarize the image.

    """
    if len(img.shape) > 2:
        img = rgb2gray(img)

    if method == "global_otsu":
        threshold = threshold_otsu(img)
        img_binary = img >= threshold

    elif method == "local_otsu":
        selem = disk(radius)
        threshold = rank.otsu(img, selem)
        img_binary = img >= threshold

    return img_binary, threshold
