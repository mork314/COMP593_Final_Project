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
    
    #Date defaults to today's date

    apod_date = datetime.now()

    #Sets acceptable date range

    start_date = datetime.strptime("1995-06-16", "%Y-%m-%d")
    today_date = datetime.now()

    #Checks to make sure a parameter was passsed, and that if so, it's a date w/in the accepted range

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

    #If the image cache already exists, function returns

    if os.path.isfile(image_cache_db):
        return
    
    #If image cache doesn't exist, image cache sql database is created

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
        
        cur.execute(create_img_tbl_query)

        con.commit()

        con.close()

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

    with open(apod_image_path, "rb") as f:
        image_hash = hashlib.sha256(f.read()).hexdigest()

    if not os.path.isfile(apod_image_path):

        image_lib.save_image
    
    #Checks whether the APOD already exists in the image cache
      
    if get_apod_id_from_db(image_hash) == 0:
        
        row_id = add_apod_to_db(title, explanation, apod_image_path, image_hash)

    else:
        row_id = get_apod_id_from_db(image_hash)

    return row_id

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

    #connects to image cache

    con = sqlite3.connect(image_cache_db)

    cur = con.cursor()

    add_apod_query = """
        INSERT INTO images
        (
        title,
        explanation,
        full_path,
        sha_256_hash
        )
        VALUES (?, ?, ?, ?);
    
    """

    #Tries to add selected apod info to cache

    try:
        cur.execute(add_apod_query, (title, explanation, file_path, sha256))
    
        con.commit()

        row_id = cur.lastrowid

        con.close()

        return row_id
    
    except:
        return 0

def get_apod_id_from_db(image_sha256):
    """Gets the record ID of the APOD in the cache having a specified SHA-256 hash value
    
    This function can be used to determine whether a specific image exists in the cache.

    Args:
        image_sha256 (str): SHA-256 hash value of APOD image

    Returns:
        int: Record ID of the APOD in the image cache DB, if it exists. Zero, if it does not.
    """

    con = sqlite3.connect(image_cache_db)

    cur = con.cursor()

    try: 
        get_id_from_sha = """
        SELECT rowid
        FROM images
        WHERE sha_256_hash = ?
        
        """

        id = cur.execute(get_id_from_sha, (image_sha256,))
    
        id = cur.fetchone()[0]

        con.close()
        
        return id    

    except:

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

    if re.search(('youtube'), image_url):
        file_extension = re.search(('hqdefault(\..*)$'), image_url).group(1)
    else:
        file_extension = re.search(('https.*\/.*\/.*\/.*\/.*(\..*)$'), image_url).group(1)


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
    
    #Queries DB for image info

    con = sqlite3.connect(image_cache_db)
    cur = con.cursor()

    cur.execute('''SELECT * FROM images WHERE rowid = ?''', (image_id,))

    image_info = cur.fetchone()

    #Put information into a dictionary
    apod_info = {
        'title': image_info[1], 
        'explanation': image_info[2],
        'file_path': image_info[3],
    }

    return apod_info

def get_all_apod_titles():
    """Gets a list of the titles of all APODs in the image cache

    Returns:
        list: Titles of all images in the cache
    """

    #connects to the database

    con = sqlite3.connect(image_cache_db)

    cur = con.cursor()

    #Gets the titles of all images in the database

    get_titles_query = """
        SELECT title FROM images 
    
    """

    cur.execute(get_titles_query)

    titles_list = []

    #Creates a list of all images in the database

    for item in cur.fetchall():

        titles_list.append(item[0])

    #Closes database connection

    con.close()

    return titles_list

if __name__ == '__main__':
    main()