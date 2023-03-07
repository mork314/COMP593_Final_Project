'''
Library for interacting with NASA's Astronomy Picture of the Day API.
'''
from sys import argv
from datetime import datetime
import sys
import requests
import re

def main():

    apod_date = argv[1]
    
    apod_info_dict = get_apod_info(apod_date)

    apod_image_url = get_apod_image_url(apod_info_dict)
    
    print(apod_image_url)

    # TODO: Add code to test the functions in this module
    #Video date 2021-02-09
    return

def get_apod_info(apod_date = datetime.today().strftime('%Y-%m-%d')):
    """Gets information from the NASA API for the Astronomy 
    Picture of the Day (APOD) from a specified date.

    Args:
        apod_date (date): APOD date (Can also be a string formatted as YYYY-MM-DD)

    Returns:
        dict: Dictionary of APOD info, if successful. None if unsuccessful
    """
    #we have apod_date
    #check if in yyyy-mm-dd
    start_date = datetime.strptime("1995-06-16", "%Y-%m-%d")
    today_date = datetime.now()
    apod_date_formatted = datetime.strptime(apod_date, "%Y-%m-%d")
    
    if date_validate(apod_date):
        
        print('correct format :D')
         #check if not before 1995-06-16
        #check if not in the future
        #print descriptive error if invalid, and quit
        if date_in_range(apod_date_formatted, start_date, today_date):
            
            print('date in range :D')

            my_key = 'DgriSg16XPnG7g7kLePDwFXFD8CZlQqbGMVZkYTS'
            
            apod_url = f"https://api.nasa.gov/planetary/apod?api_key={my_key}&date={apod_date}"

            apod_response = requests.get(apod_url).json()
                
            return apod_response
    else:
        return None

def date_validate(date):
    '''
    Ensures that a date is in YYYY-MM-DD format
    '''
    
    try:
        
        if date != datetime.strptime(date, "%Y-%m-%d").strftime('%Y-%m-%d'):
            
            raise ValueError
        
        return True
    
    except ValueError:
        
        print("Incorrect date format, please use YYYY-MM-DD")
        sys.exit()

def date_in_range(date, start, end):
    '''
    ensures that a date is within a specified range 
    '''
    
    if start <= date <= end:
        
        return True
    
    else:
        
        print("Sorry, that date is outside of the accepted range. Please enter a date from 1995-06-16 to today, inclusive.")
        sys.exit()

def get_apod_image_url(apod_info_dict):
    """Gets the URL of the APOD image from the dictionary of APOD information.

    If the APOD is an image, gets the URL of the high definition image.
    If the APOD is a video, gets the URL of the video thumbnail.

    Args:
        apod_info_dict (dict): Dictionary of APOD info from API

    Returns:
        str: APOD image URL
    """
    if apod_info_dict['media_type'] == 'image':
        
        img_url = apod_info_dict['url']
        
    elif apod_info_dict['media_type'] == 'video':

        youtube_url = apod_info_dict['url']
        
        youtube_id = re.search('embed\/(.*)\?', youtube_url)[1]

        img_url = f'http://img.youtube.com/vi/{youtube_id}/hqdefault.jpg'
        
    return img_url

if __name__ == '__main__':
    main()