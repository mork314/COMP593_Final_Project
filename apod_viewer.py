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
root.geometry('600x400')
#Gives window a title
root.title("Astronomy Picture of the Day Viewer")
#Creates calendar and adds to window

mindate = date(1995, 6, 16)
maxdate = date.today()




def open_calendar():  

    top = Toplevel(root)

    cal = Calendar(top, selectmode = 'day', mindate=mindate, maxdate=maxdate)
    cal.pack(pady=20)

    button = Button(top, text="Select This Date", command=lambda: get_selected_date(cal, top))
    button.pack()

    top.wait_window(top)

    date_selected = cal.selection_get()
        
    return date_selected

def get_selected_date(calendar, top):
    
        selected_date = calendar.selection_get()
        
        date_str = selected_date.strftime("%Y-%m-%d")
        
        top.destroy()

        print(date_str)


def get_date_and_image():

    apod_date = open_calendar()

    apod_id = apod_desktop.add_apod_to_cache(apod_date)

    apod_info = apod_desktop.get_apod_info(apod_id)

    image_path = apod_info['file_path']

    image_info = apod_info['explanation']

    display_image_and_explanation(image_path, image_info)

button = Button(root, text = "Open the Calendar to Select a Date", command=get_date_and_image)

button.pack(pady=20)

def display_image_and_explanation(image_path, image_info):
    
    


    img_to_display = Image.open(image_path)

    #Scale image to a max height of 300, width of 550

    img_to_display.thumbnail((550, 300))

    tk_image = ImageTk.PhotoImage(img_to_display)

    img_label = Label(image=tk_image)
    
    #This is a fix I found online to stop my image from being 'Garbage collected' - I guess the program decides tk_image can get thrown away
    # once we move far enough along ? Not sure

    img_label.image = tk_image

    img_label.place(relx = 0.5, rely = 0.25, anchor = 'center')

    explanation_label = Label(root, text = image_info, wraplength = 550, bg = "deep pink", fg = "yellow")

    explanation_label.place(relx = 0.5, rely = 0.85, anchor = 'center')  
    

    #scales font size w/ amount of text

    font_size = 5

    while explanation_label.winfo_reqwidth() < 550:
        font_size += 1
        explanation_label.config(font=("Arial", font_size))

    #Sets font as comic sans

    font_tuple = ("Comic Sans MS", font_size, "bold")

    explanation_label.configure(font = font_tuple)

 










#select date from calendar --> translate date into proper format for apod_desktop functions
# use apod_desktop functions to get that image, import title, description, file location to this script
# display image w/ title and description.







root.mainloop()
