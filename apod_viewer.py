from tkinter import *
import inspect
import os
import apod_desktop
from PIL import ImageTk, Image
from tkcalendar import Calendar
from datetime import date, datetime

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
    cal.pack(pady=20)

    #creates and places a button that closes the calendar window when pressed
    button = Button(top, text="Select This Date", command=lambda: top.destroy())
    button.pack()

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


def create_calendar_button():
    
    button = Button(root, text = "Open the Calendar to Select a Date", command=get_date_and_image)
    
    button.pack(pady=20)


def display_image_and_explanation(image_path, image_info):
    
    global window_width, window_height

    window_width = root.winfo_width()

    window_height = root.winfo_height()

    img_to_display = Image.open(image_path)

    #Scale image to window size

    img_to_display.thumbnail((0.9 * window_width, 0.75 * window_height))

    tk_image = ImageTk.PhotoImage(img_to_display)

    img_label = Label(image=tk_image)
    
    #This is a fix I found online to stop my image from being 'Garbage collected' - I guess the program decides tk_image can get thrown away
    # once we move far enough along ? Not sure

    img_label.image = tk_image

    img_label.place(relx = 0.5, rely = 0.25, anchor = 'center')

    explanation_label = Label(root, text = image_info, wraplength = 0.95 * window_width, bg = "deep pink", fg = "yellow")

    explanation_label.place(relx = 0.5, rely = 0.85, anchor = 'center')  
    
    

    #scales font size w/ amount of text & window size - weird things happened when it was a float value so we're just doing this :D

    font_size = int(12 * (window_height / 800))

    while explanation_label.winfo_reqwidth() < 0.95 * window_width:
        font_size += 1
        explanation_label.config(font=("Arial", font_size))

    #Sets font as comic sans

    font_tuple = ("Comic Sans MS", font_size, "bold")

    explanation_label.configure(font = font_tuple)

 


#select date from calendar --> translate date into proper format for apod_desktop functions
# use apod_desktop functions to get that image, import title, description, file location to this script
# display image w/ title and description.



create_calendar_button()



root.mainloop()
