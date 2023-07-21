###############################################################
# Digital billboard advertising on a display using Tkinter
# Media files are imported from a USB device (jpeg or png)
# USB stick needs to have bilboard.json in it's root directory
# image files in the root directory will be listed and displayed automatically
# Files will be resized to screen resolution
# Settings configurable in json file on the USB
# Use single display on HDMI0
# v1
# Creator: Patrik Horemans
# Copyrights: free to use
################################################################
# default settings
settings_json = [{"default_delay":3}]
################################################################


import os
import json
from tkinter import *
from PIL import ImageTk, Image
import time
import signal
user_env = "koekoek" #depends on RPI installation. Default this user is Pi
file_types = ["jpeg","png","JPEG","PNG"]
files_to_show = []
settings_file = "bilboard.json"
msg_prev_time = time.time() - 5000
msg_curr = 0
msg_to_show = ""
state = 0
retries = 0



#create window object
win = Tk()
#win.geometry("400x300")
win.attributes('-fullscreen',True)
#Get the current screen width and height
screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()
print("Screenwidth & height:",screen_width,"x",screen_height)
label1 = Label(win, text="Starting, please wait 10 secs", font=("APhont",50), wraplength = 900)
label1.place(x=10,y=10)
win.update()


def printw(text_to_display):
    global label1
    label1.config(text=text_to_display)
    label1.place(x=10,y=10)
    win.update()

def read_settings(a_json):
    #read settings from json variable
    try:
        global msg_delay
        print("file to read settings from:",a_json)
        msg_delay = a_json['delay']
        return True
    except:
        print("Something went wrong reading from billboard.json, format maybe? should be {\"delay\":5} for example")
        printw("Something went wrong reading from billboard.json, format maybe? should be {\"delay\":5} for example")
        return False

while True:
    if state ==0:
        print("Step 1: Look for USB drives, wait 10 sec")
        printw("Step 1-5: Look for USB drives, wait 10 sec")
        time.sleep(10)
        files_to_show = []
        try:
            drives = os.listdir("/media/" + user_env)
            if len(drives) > 0:
                state = 1
                printw("USB drive(s) found:" + str(drives))
                print(drives)
                retries = 0
            else:
                retries = retries + 1
                printw("No USB drives found, retry in 10 sec attempt:" + str(retries))
        except:
            retry = retry + 1
            printw('could not list USB drives, will retry in 10 sec, attempt:' + str(retries))
        time.sleep(2)

    if state == 1:
        print("Step 2: Look for billboard.json file on USB drive")
        printw("Step 2-5: Look for billboard.json file on USB drive")
        time.sleep(2)
        for drive in drives:
            try:
                files = os.listdir("/media/" + user_env + "/" + drive)
                if settings_file in files:
                    USB_path = "/media/" + user_env + "/" + drive
                    USB_files = files
                    print("bilboard usb found on " + USB_path)
                    printw("Valid USB drive found")
                    state = 2
                    break
                else:
                    print("no bilboard usb found")
                    printw("no bilboard usb found")
                    state = 0
            except:
                print("could not open file or directory, media missing?")
                printw("could not open file or directory, media missing? Starting over in 10 sec.")
                state = 0
                
        time.sleep(2)

    if state == 2:
        print("Step 3: Read billboard.json settings")
        printw("Step 3-5: Read billboard.json settings")
        try:
            f = open(USB_path + "/" + settings_file, "r")
            settings = f.read()
            settings_json = json.loads(settings)
            f.close
            if read_settings(settings_json):
                state = 3
        except:
            print("Could not read billboard.json, start over...")
            printw("Could not read billboard.json, start over...")
            state = 0
            
        time.sleep(2)
            
    if state == 3:
        print("Step 4: Look for valid files of type:",file_types)
        printw("Step 4-5: Look for valid files of type:"+ str(file_types))
        for file in USB_files:
            for file_type in file_types:
                if file_type in file:
                    if not(file.startswith(".")):
                        files_to_show.append(file)
        print(files_to_show)
        time.sleep(2)
        if len(files_to_show) > 0:
            printw("step 5-5:Valid files to display found, start showing")
            state = 4
        else:
            printw("No valid files to display found, restarting, please wait 10 sec")
            state = 0
        time.sleep(2)                    
                


    if state == 4:
        if time.time() - msg_prev_time > msg_delay:
            msg_prev_time = time.time()
            print("showing message", msg_curr+1 , "from", len(files_to_show))
            try:
                image =Image.open(USB_path + "/" + files_to_show[msg_curr])
                resize_image =image.resize((screen_width,screen_height))
                msg_to_show = ImageTk.PhotoImage(resize_image)
                lbl_back_picture= Label(win, image = msg_to_show)
                lbl_back_picture.place(x=0,y=0)
                msg_curr += 1
                if msg_curr == len(files_to_show):
                    msg_curr = 0
            except:
                try:
                    lbl_back_picture.place_forget()
                except:
                    print("no image displayed, could not forget")
                print("could not display files, maybe valid USB missing?")
                printw("could not display files, maybe valid USB missing? Start over, please wait 10 seconds")
                state = 0
        win.update()
        
    
