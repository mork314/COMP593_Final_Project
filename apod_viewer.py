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
import ctypes

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

global image_path

image_path = ''

root.image = image_path



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

def get_date_and_image_cal():

    screen_reset()

    apod_date = open_calendar()

    apod_id = apod_desktop.add_apod_to_cache(apod_date)

    apod_info = apod_desktop.get_apod_info(apod_id)

    image_path = apod_info['file_path']

    #was having trouble getting desktop button to remember image_path existed - this seems to fix it

    root.image = image_path

    image_info = apod_info['explanation']

    display_image_and_explanation(image_path, image_info)

def create_calendar_button():
    
    cal_button = Button(root, text = "Open the Calendar to Select a Date", command=get_date_and_image_cal)
    
    cal_button.grid(column = 1, row = 2, sticky = "nsew")

def get_date_and_image_dropdown(apod_title):
    
    screen_reset()
    
    con = sqlite3.connect(apod_desktop.image_cache_db)

    cur = con.cursor()

    #Fetches the database ID of the image with the chosen title

    get_image_query = """
        SELECT id FROM images
        WHERE title = ?
    
    """

    cur.execute(get_image_query, (apod_title,))

    apod_id = cur.fetchone()[0]

    apod_info = apod_desktop.get_apod_info(apod_id)

    image_path = apod_info['file_path']

    root.image = image_path

    image_info = apod_info['explanation']

    display_image_and_explanation(image_path, image_info)

    con.close()   

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

    img_label.grid(column = 0, row = 0, columnspan = 3, sticky = "nsew")

    explanation_label = Label(root, text = image_info, wraplength = window_width, bg = "deep pink", fg = "yellow")

    explanation_label.grid(column = 0, row = 1, columnspan = 3, sticky = "nsew")
    
    #scales font size w/ amount of text & window size - weird things happened when it was a float value so we're just doing this :D

    font_size = 5

    min_height = 0.2 * window_height

    #Increases font size to fit the size of the window

    while explanation_label.winfo_reqheight() < min_height:
        font_size += 1
        explanation_label.config(font=("Comic Sans MS", font_size))
    
    return image_path
    
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

    img_label.grid(column = 0, columnspan = 3, row = 1, padx = 10, pady = 10, sticky = "nsew")

def dropdown_menu():
    
    #Gets all apod titles
    
    titles_list = apod_desktop.get_all_apod_titles()

    #Creates a dropdown menu containing those titles

    global dropdown_group

    dropdown_group = LabelFrame(root, height = int(window_height / 10), text = "View Cached Image")
    dropdown_group.grid(column = 0, row = 2, sticky = "nsew")

    Label(dropdown_group, text = "Select an image from the database :").grid(column = 0, row = 0, sticky = "nsew")

    n = StringVar()

    image_chosen = Combobox(dropdown_group, values = titles_list, width = 27, textvariable = n)

    image_chosen.grid(column=1, row = 0, sticky = "nsew")

    #def fetch_image():

       # print(image_chosen.get())

    select_button = Button(dropdown_group, text = "Select this image", command=lambda: get_date_and_image_dropdown(image_chosen.get()))
    select_button.grid(column = 2, row = 0, sticky = "nsew")

def screen_reset():

    for widget in root.winfo_children():
        widget.destroy()
    
    create_calendar_button()

    dropdown_menu()

    create_desktop_button()

def dynamic_resize():

    #By giving the rows weight, they expand to fill available space
    
    for row_num in range(0, 2):
        root.rowconfigure(row_num, weight = 1)
        dropdown_group.rowconfigure(row_num, weight = 1)
    
    for column_num in range(0, 2):
        root.columnconfigure(column_num, weight = 1)
        dropdown_group.columnconfigure(column_num, weight = 1)

def set_desktop_image(image_path):

    image_lib.set_desktop_background_image(image_path)

def create_desktop_button():

    desk_button = Button(root, text = "Set the current image as your desktop background", command=lambda: set_desktop_image(root.image))
    
    desk_button.grid(column = 2, row = 2, sticky = "nsew")

def set_window_and_task_image():

    #Saves the desired image
    
    image_data = image_lib.download_image(r'https://cdn-icons-png.flaticon.com/512/3306/3306571.png')

    image_path = script_dir + '\window_default.jpg'

    image_lib.save_image_file(image_data, image_path)

    #turns the image into a .ico photoimage thingy and saves it

    ico = Image.open(image_path)

    ico.save(image_path, format='ICO')

    #Sets the window icon

    root.iconbitmap(False, image_path)

    #I do not know how this works, but it uses the ctypes library to change the taskbar image.

    window_handle = ctypes.windll.user32.GetParent(root.winfo_id())

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("Tkinter_id")

    ctypes.windll.user32.SetClassLongW(window_handle, -14, ctypes.windll.shell32.Shell_GetCachedImageIndexW(image_path, 0, 0x00000000))




#select date from calendar --> translate date into proper format for apod_desktop functions
# use apod_desktop functions to get that image, import title, description, file location to this script
# display image w/ title and description.



#displays default image + menu options

make_home_screen()

set_window_and_task_image()

dropdown_menu()

create_calendar_button()

create_desktop_button()

dynamic_resize()

root.mainloop()