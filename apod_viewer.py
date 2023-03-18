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
    
    def get_selected_date():
    
        selected_date = cal.selection_get()
        
        date_str = selected_date.strftime("%Y-%m-%d")
        
        top.destroy()

        print(date_str)

        return date_str

    top = Toplevel(root)

    cal = Calendar(top, selectmode = 'day', mindate=mindate, maxdate=maxdate)
    cal.pack(pady=20)

    button = Button(top, text="Select This Date", command=get_selected_date)
    button.pack()

def get_date_and_image():

    open_calendar()

    apod_id = apod_desktop.add_apod_to_cache(apod_date)

    print(apod_id)

button = Button(root, text = "Open the Calendar to Select a Date", command=get_date_and_image)

button.pack(pady=20)




#OK THIS DISPLAYS AN IMAGE OF YOUR CHOICE BIG MONEY
current_apod = Image.open(r'C:\Users\markn\OneDrive\Documents\GitHub\COMP593_Final_Project\image_cache_directory\Earth_or_Mars.jpg')
test = ImageTk.PhotoImage(current_apod)

img_label = Label(image=test)
desc_label = Label(root, text = 'DESCRIPTION', bg = "deep pink", fg = "yellow")

img_label.pack()

#NOT REALLY SURE HOW THIS CENTERING STUFF WORKS - THIS CODE PLACES THE ANCHOR IN THE UPPER LEFT CORNER OF THE SCREEN

desc_label.place(relx = 0.5, rely = 0.925, anchor = 'center')

#select date from calendar --> translate date into proper format for apod_desktop functions
# use apod_desktop functions to get that image, import title, description, file location to this script
# display image w/ title and description.

#alternatively, just select image from cache by title.

#Sets font as comic sans

font_tuple = ("Comic Sans MS", 30, "bold")

desc_label.configure(font = font_tuple)


root.mainloop()
