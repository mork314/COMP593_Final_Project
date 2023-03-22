from tkinter.ttk import *
from tkinter import *
import inspect
import os
import apod_desktop
from PIL import ImageTk, Image
from tkcalendar import Calendar
from datetime import date, datetime
import image_lib
import sqlite3

# Determine the path and parent directory of this script
script_path = os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)
script_dir = os.path.dirname(script_path)

# Initialize the image cache
apod_desktop.init_apod_cache(script_dir)

# TODO: Create the GUI
#Creates window
root = Tk()
#Sets size of window
window_width = 1200

window_height = 800

root.geometry(f'{window_width}x{window_height}')
#Gives window a title
root.title("Astronomy Picture of the Day Viewer")
#Creates calendar and adds to window

#These variables will be used later to limit the range of the calendar
mindate = date(1995, 6, 16)
maxdate = date.today()




def open_calendar():  

    #Opens a 'top level' window
    top = Toplevel(root)

    #creates a calendar widget in the top level window
    cal = Calendar(top, selectmode = 'day', mindate=mindate, maxdate=maxdate)
    cal.grid(column = 0, row = 0)

    #creates and places a button that closes the calendar window when pressed
    button = Button(top, text="Select This Date", command=lambda: top.destroy())
    button.grid(column = 1, row = 1)

    #waits until the top window is closed to execute the next line

    top.wait_window(top)

    date_selected = cal.selection_get()
        
    return date_selected


def get_date_and_image():

    for widget in root.winfo_children():
        widget.destroy()

    apod_date = open_calendar()

    apod_id = apod_desktop.add_apod_to_cache(apod_date)

    apod_info = apod_desktop.get_apod_info(apod_id)

    image_path = apod_info['file_path']

    image_info = apod_info['explanation']

    display_image_and_explanation(image_path, image_info)

    create_calendar_button()

    dropdown_menu()


def create_calendar_button():
    
    button = Button(root, text = "Open the Calendar to Select a Date", command=get_date_and_image)
    
    button.grid(column = 2, row = 2)


def display_image_and_explanation(image_path, image_info):
    
    global window_width, window_height

    window_width = root.winfo_width()

    window_height = root.winfo_height()

    img_to_display = Image.open(image_path)

    #Scale image to window size

    img_to_display.thumbnail((window_width, 0.7 * window_height))

    tk_image = ImageTk.PhotoImage(img_to_display)

    img_label = Label(image=tk_image)
    
    #This is a fix I found online to stop my image from being 'Garbage collected' - I guess the program decides tk_image can get thrown away
    # once we move far enough along ? Not sure

    img_label.image = tk_image

    img_label.grid(column = 0, row = 0, columnspan = 3, sticky = "WE")

    explanation_label = Label(root, text = image_info, wraplength = window_width, bg = "deep pink", fg = "yellow")

    explanation_label.grid(column = 0, row = 1, columnspan = 3, sticky = "WE")
    
    #scales font size w/ amount of text & window size - weird things happened when it was a float value so we're just doing this :D

    font_size = 5

    min_height = 0.2 * window_height

    while explanation_label.winfo_reqheight() < min_height:
        font_size += 1
        explanation_label.config(font=("Comic Sans MS", font_size))
    

def make_home_screen():

    #Downloads the desired default image

    image_data = image_lib.download_image(r'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.models-resource.com%2Fresources%2Fbig_icons%2F48%2F47830.png&f=1&nofb=1&ipt=4457110841d33186f65927ad4fd111c44c90daaa90154770bdc765b0edba9cf1&ipo=images')
    
    image_path = script_dir + '\minion_default.jpg'

    image_lib.save_image_file(image_data, image_path)

    #Displays selected image

    img_to_display = Image.open(image_path)

    img_to_display.thumbnail((window_width, window_height))

    tk_image = ImageTk.PhotoImage(img_to_display)

    img_label = Label(image = tk_image)

    img_label.image = tk_image

    img_label.grid(column = 0, columnspan = 3, row = 1, padx = 10, pady = 10, sticky = "WE")

def dropdown_menu():

    con = sqlite3.connect(apod_desktop.image_cache_db)

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

    #Creates a dropdown menu containing those titles

    dropdown_group = LabelFrame(root, height = int(window_height / 10), text = "View Cached Image")
    dropdown_group.grid(column = 0, row = 2)

    Label(dropdown_group, text = "Select an image from the database :").grid(column = 0, row = 0)

    n = StringVar()

    image_chosen = Combobox(dropdown_group, width = 27, textvariable = n)

    image_chosen['values'] = titles_list

    image_chosen.grid(column=1, row = 0)
    
    image_chosen.set("Select image")

    def get_selection(*arg):
        
        selected_title = titles_list[image_chosen.current()]
        
        return selected_title

    n.trace('w', get_selection)
      
    con.close()



#select date from calendar --> translate date into proper format for apod_desktop functions
# use apod_desktop functions to get that image, import title, description, file location to this script
# display image w/ title and description.

dropdown_menu()

#displays default image + menu options

make_home_screen()

create_calendar_button()

root.mainloop()


