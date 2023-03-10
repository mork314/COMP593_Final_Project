""" 
COMP 593 - Final Project

Description: 
  Downloads NASA's Astronomy Picture of the Day (APOD) from a specified date
  and sets it as the desktop background image.

Usage:
  python apod_desktop.py [apod_date]

Parameters:
  apod_date = APOD date (format: YYYY-MM-DD)
"""
from datetime import date
import os
import image_lib
import inspect
import apod_api
from sys import argv
from datetime import datetime
import re
import sqlite3
import image_lib
import hashlib


# Global variables
image_cache_dir = os.path.dirname(argv[0]) + '\image_cache_directory'
image_cache_db = image_cache_dir + '\image_cache_db.db'

def main():
    ## DO NOT CHANGE THIS FUNCTION ##
    # Get the APOD date from the command line
    apod_date = get_apod_date()    

    # Get the path of the directory in which this script resides
    script_dir = get_script_dir()

    # Initialize the image cache
    init_apod_cache(script_dir)

    # Add the APOD for the specified date to the cache
    apod_id = add_apod_to_cache(apod_date)

    # Get the information for the APOD from the DB
    apod_info = get_apod_info(apod_id)

    # Set the APOD as the desktop background image
    if apod_id != 0:
        image_lib.set_desktop_background_image(apod_info['file_path'])

def get_apod_date():
    """Gets the APOD date
     
    The APOD date is taken from the first command line parameter.
    Validates that the command line parameter specifies a valid APOD date.
    Prints an error message and exits script if the date is invalid.
    Uses today's date if no date is provided on the command line.

    Returns:
        date: APOD date
    """
        
    apod_date = datetime.now()

    start_date = datetime.strptime("1995-06-16", "%Y-%m-%d")
    today_date = datetime.now()
    if len(argv) > 1:

        if apod_api.date_validate(argv[1]) and apod_api.date_in_range(argv[1], start_date, today_date):
            
            apod_date = date.fromisoformat(argv[1])
    
    return apod_date

def get_script_dir():
    """Determines the path of the directory in which this script resides

    Returns:
        str: Full path of the directory in which this script resides
    """
    ## DO NOT CHANGE THIS FUNCTION ##
    script_path = os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)
    return os.path.dirname(script_path)

def init_apod_cache(parent_dir):
    """Initializes the image cache by:
    - Determining the paths of the image cache directory and database,
    - Creating the image cache directory if it does not already exist,
    - Creating the image cache database if it does not already exist.
    
    The image cache directory is a subdirectory of the specified parent directory.
    The image cache database is a sqlite database located in the image cache directory.

    Args:
        parent_dir (str): Full path of parent directory    
    """
    global image_cache_dir
    global image_cache_db
    if not os.path.exists(image_cache_dir):
        os.mkdir(image_cache_dir)

    if os.path.isfile(image_cache_db):
        return
    
    else:
        con = sqlite3.connect(image_cache_db)
        cur = con.cursor()
        create_img_tbl_query = """
        CREATE TABLE IF NOT EXISTS images
        (
            id              INTEGER PRIMARY KEY,
            title           TEXT NOT NULL,
            explanation     TEXT NOT NULL,
            full_path       TEXT NOT NULL,
            sha_256_hash    TEXT NOT NULL
        );      
        
        """



def add_apod_to_cache(apod_date):
    """Adds the APOD image from a specified date to the image cache.
     
    The APOD information and image file is downloaded from the NASA API.
    If the APOD is not already in the DB, the image file is saved to the 
    image cache and the APOD information is added to the image cache DB.

    Args:
        apod_date (date): Date of the APOD image

    Returns:
        int: Record ID of the APOD in the image cache DB, if a new APOD is added to the
        cache successfully or if the APOD already exists in the cache. Zero, if unsuccessful.
    """
    apod_date = re.search(('.*\-.*\-..'), apod_date.isoformat()).group()
    print("APOD date:", apod_date)
    #Download the APOD information from the NASA API
    apod_info_dict = apod_api.get_apod_info(apod_date)
    
    apod_image_url = apod_api.get_apod_image_url(apod_info_dict)
    
    #Downloads the apod image
    
    downloaded_image = image_lib.download_image(apod_image_url)

    title = apod_info_dict['title']

    apod_image_path = determine_apod_file_path(title, apod_image_url)
   
    #Saves the file to the computer

    image_lib.save_image_file(downloaded_image, apod_image_path)
    
    explanation = apod_info_dict['explanation']

    image_hash = hashlib.sha256(apod_info_dict).hexdigest()

    add_apod_to_db(title, explanation, apod_image_path, image_hash)

    # TODO: Check whether the APOD already exists in the image cache
    # TODO: Save the APOD file to the image cache directory
    # TODO: Add the APOD information to the DB
    return 0

def add_apod_to_db(title, explanation, file_path, sha256):
    """Adds specified APOD information to the image cache DB.
     
    Args:
        title (str): Title of the APOD image
        explanation (str): Explanation of the APOD image
        file_path (str): Full path of the APOD image file
        sha256 (str): SHA-256 hash value of APOD image

    Returns:
        int: The ID of the newly inserted APOD record, if successful.  Zero, if unsuccessful       
    """


    # TODO: Complete function body



    return 0

def get_apod_id_from_db(image_sha256):
    """Gets the record ID of the APOD in the cache having a specified SHA-256 hash value
    
    This function can be used to determine whether a specific image exists in the cache.

    Args:
        image_sha256 (str): SHA-256 hash value of APOD image

    Returns:
        int: Record ID of the APOD in the image cache DB, if it exists. Zero, if it does not.
    """
    # TODO: Complete function body
    return 0

def determine_apod_file_path(image_title, image_url):
    """Determines the path at which a newly downloaded APOD image must be 
    saved in the image cache. 
    
    The image file name is constructed as follows:
    - The file extension is taken from the image URL
    - The file name is taken from the image title, where:
        - Leading and trailing spaces are removed
        - Inner spaces are replaced with underscores
        - Characters other than letters, numbers, and underscores are removed

    For example, suppose:
    - The image cache directory path is 'C:\\temp\\APOD'
    - The image URL is 'https://apod.nasa.gov/apod/image/2205/NGC3521LRGBHaAPOD-20.jpg'
    - The image title is ' NGC #3521: Galaxy in a Bubble '

    The image path will be 'C:\\temp\\APOD\\NGC_3521_Galaxy_in_a_Bubble.jpg'

    Args:
        image_title (str): APOD title
        image_url (str): APOD image URL
    
    Returns:
        str: Full path at which the APOD image file must be saved in the image cache directory
    """
    
    global image_cache_dir

    apod_image_search = re.search(('\..*$'), image_url)
    
    file_extension = apod_image_search.group()

    #Removes leading and trailing whitespace
    image_title = image_title.strip()
    #Replaces inner spaces with underscores
    image_title = re.sub('\s', '_', image_title)
    #Replaces characters other than letters, numbers, and underscores
    image_title = re.sub(r'[^A-Za-z0-9_]', '', image_title)
    
    image_path = f"{image_cache_dir}\\{image_title}{file_extension}"

    print(image_path)

    return image_path

def get_apod_info(image_id):
    """Gets the title, explanation, and full path of the APOD having a specified
    ID from the DB.

    Args:
        image_id (int): ID of APOD in the DB

    Returns:
        dict: Dictionary of APOD information
    """
    # TODO: Query DB for image info
    # TODO: Put information into a dictionary
    apod_info = {
        #'title': , 
        #'explanation': ,
        'file_path': 'TBD',
    }
    return apod_info

def get_all_apod_titles():
    """Gets a list of the titles of all APODs in the image cache

    Returns:
        list: Titles of all images in the cache
    """
    # TODO: Complete function body
    # NOTE: This function is only needed to support the APOD viewer GUI
    return

if __name__ == '__main__':
    main()