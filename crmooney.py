#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

from dotenv import load_dotenv

import utils
import utils_flickr
import utils_image


__author__ = "Fatma Imamoglu"
__email__ = "fatma@berkeley.edu"
__status__ = "Development"


def apply_mooney_transform(
    img, imagepath, imgname, transformations, url=None, photo_id=None
):
    """Given an image, calls the transformations needed to create the Mooney of
    it.

    Input:
        img: n-dim image
        imagepath: parent dir of 'img'
        imgname: the filename of 'img'
        transformations: dictionary with important transformation parameters
        url: if the image was downloaded, the url as a string
        photo_id: an id assigned to the image

    Returns:
        dictionary: A dictionary of a single Mooney images along with the threshold value,
            its original path and original image name.
    """

    assert isinstance(
        transformations, dict
    ), "'transformations' argument has to be a dict"

    image_size = transformations.get("image_size", (400, 400))
    resize = transformations.get("resize", False)
    smooth_sigma = transformations.get("smooth_sigma", 6)
    threshold_method = transformations.get("threshold_method", "global_otsu")

    # Convert to gray scale image
    if len(img.shape) > 2:
        img = utils_image.rgb2gray(img)
        fname = os.path.join(
            mooneypath, imgname.split(".")[0] + "_g." + imgname.split(".")[1]
        )
        utils_image.save_img(img, fname)

    # Resize image
    if resize:
        img = utils_image.resize(img, size=image_size)
        fname = os.path.join(
            mooneypath, imgname.split(".")[0] + "_gr." + imgname.split(".")[1]
        )
        utils_image.save_img(img, fname)

    # Smooth image
    img = utils_image.gauss_filter(img, sigma=smooth_sigma)
    fname = os.path.join(
        mooneypath, imgname.split(".")[0] + "_s." + imgname.split(".")[1]
    )
    utils_image.save_img(img, fname)

    # Create Mooney image
    img, threshold = utils_image.threshold_img(img, method=threshold_method)
    fname = os.path.join(
        mooneypath, imgname.split(".")[0] + "_m." + imgname.split(".")[1]
    )
    utils_image.save_img(img, fname)

    # Store resulting image in a dict
    return {
        "img_id": photo_id,
        "img_name": imgname.split(".")[0],
        "img_mooney": img,
        "threshold": threshold,
        "threshold_method": threshold_method,
        "resize": resize,
        "smooth_sigma": smooth_sigma,
        "url": url,
        "mooneypath": mooneypath,
        "imagepath": imagepath,
    }


def crmooney_fromdb(
    api_key,
    api_secret,
    search_words,
    imagepath="",
    mooneypath="",
    dbname="flickr",
    search_tags=None,
    license="2",
    size="original",
    content_type=1,
    media="photos",
    pages_to_get=None,
    per_page=50,
    resize=False,
    smooth_sigma=6,
    image_size=(400, 400),
    threshold_method="global_otsu",
):
    """Given an API key and secret, and search words, download images from
    image db, create Mooney images and save Mooney images in the directory
    specified with mooneypath.

    Input:
        api_key: API key of the online image database.
        api_secret: API secret of the online image database.
        search_words: A list of search words. These words will be used in the specified
            image database as search words.
        imagepath: Path where the downloaded images should be saved.
        mooneypath: Path where the Mooney images should be saved.
        dbname: Online image database identifier. Default: 'flickr' (others to be implemented.)
        search_tags: Similar to search words. Could be used to further resitrict the search results.
        license: String of numbers. (check: utils_flickr.get_license_info())

    Returns:
        imgs_mooney: A dictionary of Mooney images along with the threshold value,
            its original path and original image name.
    """

    if search_tags is None:
        search_tags = []
    if pages_to_get is None:
        pages_to_get = [1, 2]

    if imagepath == "":
        imagepath = os.getcwd()

    transformations = {
        "image_size": image_size,
        "resize": resize,
        "smooth_sigma": smooth_sigma,
        "threshold_method": threshold_method,
    }

    # create imagepath dir (could raise an exception if folder permissions are restrictive)
    utils_image.mkdir(imagepath)

    ## Connect to API
    if dbname == "flickr":  ### Else to come
        ## Use API implementation by Beej's Python Flickr API
        api = utils.connect_api(dbname, api_key, api_secret)

        ## Print general license information
        utils_flickr.get_license_info(api)
        print(
            f"You choice of license: {license}. \n Set 'license' if you want to change this."
        )

    imgs_mooney = []
    photo_meta = []
    for search_word in search_words:

        search_tag = search_word
        print(f"Image search in {dbname}. \n \t search word: \t {search_word}")

        ## Search and store metadata
        pages = [
            api.photos.search(
                text=search_word,
                tag=search_tag,
                license=license,
                content_type=content_type,
                media=media,
                per_page=per_page,
                page=p,
            )
            for p in pages_to_get
        ]
        for page in pages:
            for photo in page["photos"]["photo"]:
                meta = utils_flickr.get_metadata(api, photo)
                photo_meta.append(meta)

    ## Save metadata
    filename = os.path.join(imagepath, "flickr_download_metadata")
    utils.write_metadata(photo_meta, filename, file_format="json")

    ## Download and create Mooney images
    counter = 1
    for photo in photo_meta:
        if counter % 50 == 0:
            print(f"\t\t {counter}/{len(photo_meta)} downloaded.")
        if size == "original":
            url = photo["original"]["source"]
        elif size == "large_square":
            url = photo["large_square"]["source"]

        filename = os.path.join(imagepath, url.split("/")[-1])
        imgname = os.path.basename(filename)

        # Download image
        utils.get_image(url, filename)

        # Load image
        img = utils_image.load_imgs(filename)
        img = img[imgname]

        imgs_mooney.append(
            apply_mooney_transform(
                img,
                imagepath,
                imgname,
                transformations,
                url=url,
                photo_id=photo["photo_id"],
            )
        )

        counter += 1

    if imgs_mooney:
        print(
            f"{len(imgs_mooney)} images are downloaded in {imagepath}.\n"
            + f"Corresponding Mooneys are in {mooneypath}."
        )

    return imgs_mooney, photo_meta


def crmooney_frompath(
    filename,
    mooneypath="",
    resize=False,
    smooth_sigma=6,
    image_size=(400, 400),
    threshold_method="global_otsu",
):
    """Given a path create and save Mooney images in the directory specified
    with.

    Input:
        filename: Can be a directory (in which case all the .JPG files will be converted to Mooney)
            or the path of the jpg file.
        mooneypath: Path to save the final Mooney image.

    Returns:
        imgs_mooney: A dictionary of Mooney images along with the threshold value,
            its original path and original image name.
    """

    if mooneypath == "":
        if not os.path.dirname(filename) == "":
            mooneypath = os.path.dirname(filename)
        else:
            mooneypath = os.getcwd()

    transformations = {
        "image_size": image_size,
        "resize": resize,
        "smooth_sigma": smooth_sigma,
        "threshold_method": threshold_method,
    }

    # Load image
    imgs = utils_image.load_imgs(filename)

    imgs_mooney = []
    for imgname, img in imgs.items():
        imgs_mooney.append(
            apply_mooney_transform(
                img,
                os.path.dirname(filename),
                os.path.basename(imgname),
                transformations,
            )
        )

    if imgs_mooney:
        print(f"{len(imgs_mooney)} Mooney images are in {mooneypath}.")

    return imgs_mooney


if __name__ == "__main__":

    ## Use search words to search images in Flickr image database
    try:
        os.path.exists(sys.argv[1])
        print(f"Search words read from file: {sys.argv[1]}")
        search_words = utils.read_file(sys.argv[1])
    except (IOError, IndexError):
        search_words = ["cat"]

    # Flickr-API authentication keys.
    # Get your own before using this from https://www.flickr.com/services/api/
    # API_KEY = ""
    # API_SECRET = ""
    load_dotenv()
    API_KEY = os.getenv("API_KEY")
    API_SECRET = os.getenv("API_SECRET")
    try:
        assert API_KEY and API_SECRET

        print(
            "Good news, you have API_KEY and API_SECRET defined. You are ready to go."
        )

        license = (
            "2"
        )  # 2: "Attribution-NonCommercial License", 4: "Attribution License"
        imagepath = os.path.join(os.getcwd(), "images", "flickr")
        mooneypath = os.path.join(imagepath, "mooney")

        imgs, metadata = crmooney_fromdb(
            api_key=API_KEY,
            api_secret=API_SECRET,
            search_words=search_words,
            imagepath=imagepath,
            mooneypath=mooneypath,
            dbname="flickr",
            search_tags=[],
            license=license,
            size="original",
            content_type=1,
            media="photos",
            pages_to_get=[1],
            per_page=2,
            resize=False,
            smooth_sigma=6,
            image_size=(400, 400),
            threshold_method="global_otsu",
        )

    except AssertionError:
        ## Create images from a given path
        print(
            "You need an API_KEY and API_SECRET to continue.\n"
            + "Check https://www.flickr.com/services/api"
        )

        imagepath = os.path.join(os.getcwd(), "images")

        print("------------ or:\n")
        choice = (
            input(
                f"Press [ENTER] if you want to convert images in {imagepath}.\n"
                + "Enter 'q' or 'quit' and press [ENTER] to cancel.\n"
            )
            or imagepath
        )

        print(choice)

        if choice in ("q", "quit"):
            sys.exit()

        assert os.path.isdir(choice), f"Entered path '{choice}' is not a folder"
        imagepath = choice

        mooneypath = os.path.join(imagepath, "mooney")
        imgs = crmooney_frompath(
            imagepath,
            mooneypath=mooneypath,
            resize=False,
            smooth_sigma=6,
            image_size=(400, 400),
            threshold_method="global_otsu",
        )
