import cv2
from PIL import Image, ImageTk
from tkinter import *  # Importing everything in tkinter
import tkinter as tk  # Importing specific part of tkinter
from tkinter import ttk  # Importing specific part of tkinter
from movement import *  # Importing everything from movement
import threading
from PIL import Image, ImageTk
from logdefiner import get_log_name
from tkinter import scrolledtext
from video import road_stream, road_overlay_stream

filename = get_log_name()


def backend(name):  # Function thta creates window titled the first name of the username that logged in
    inner = Tk()  # Creating window
    inner.title("Welcome " + name)  # Creating title
    inner.geometry("1600x1080")  # Setting dimensions

    frame1 = tk.Frame(inner, borderwidth=0, relief='ridge')  # Creating top left frame
    frame1.grid(row=0, column=0, padx=(150, 150), pady=(70, 70))
    frame2 = tk.Frame(inner, borderwidth=0, relief='ridge')  # Creating top right frame
    frame2.grid(row=0, column=1, padx=(150, 150), pady=(70, 70))
    frame3 = tk.Frame(inner, borderwidth=0, relief='ridge')  # Creating bottom left frame
    frame3.grid(row=1, column=0, padx=(150, 150), pady=(70, 70))
    frame4 = tk.Frame(inner, borderwidth=0, relief='ridge', highlightbackground="black",highlightthickness=5)  # Creating bottom right
    frame4.grid(row=1, column=1, padx=(150, 150), pady=(70, 70))

    def updatelog():  # Function for log updating
        global logtext
        logtext = ""  # Initializing varible
        with open(filename, 'r') as f:  # Opening log.txt
            lines = f.readlines()  # Reading last 14 lines
            for line in lines:  # Iterating lines
                line = str(line)
                logtext = line  # Adding each iteration line to a variable
        return (logtext)  # Returning chunk of log text

    w4 = scrolledtext.ScrolledText(frame4, wrap=tk.WORD, width=40, height=17, font=("Inter", 15))
    w4.insert(tk.INSERT, str(updatelog()))
    w4.grid(row=0, column=0)
    w4.configure(state='disabled')

    fwd = Button(frame2, text='↑ ', height=3, width=8, font="90", fg="black",command=lambda: forward_and_update())  # Making forward button
    fwd.grid(row=0, column=1, columnspan=2)

    lft = Button(frame2, text='←', height=3, width=5, font="45", fg="black",command=lambda: left_and_update())  # Making left button
    lft.grid(row=1, column=0)

    rgt = Button(frame2, text='→', height=3, width=5, font="45", fg="black",command=lambda: right_and_update())  # Making right button
    rgt.grid(row=1, column=3)

    bwd = Button(frame2, text='↓', height=3, width=8, font="45", fg="black",command=lambda: backward_and_update())  # Making backward button
    bwd.grid(row=2, column=1, columnspan=2)

    ply = Button(frame2, text='▶', height=3, width=2, font="45", fg="Green",command=lambda: go_and_update())  # Making go button
    ply.grid(row=1, column=1)

    stp = Button(frame2, text='⏸', height=3, width=2, font="45", fg="Red",command=lambda: stop_and_update())  # Making stop button
    stp.grid(row=1, column=2)

    def forward_and_update():  # Importing forward command and adding log update command to it to send to buttons
        forward()
        w4.configure(state='normal')  # state normal allows to write to text box
        w4.insert(tk.INSERT, str(updatelog()))  # writes with updated log line
        w4.configure(state='disabled')  # state disabled makes it read only
        w4.yview(END)  # auto scrolls to end of code

    def left_and_update():  # Importing left command and adding log update command to it to send to buttons
        left()
        w4.configure(state='normal')
        w4.insert(tk.INSERT, str(updatelog()))
        w4.configure(state='disabled')
        w4.yview(END)

    def right_and_update():  # Importing right command and adding log update command to it to send to buttons
        right()
        w4.configure(state='normal')
        w4.insert(tk.INSERT, str(updatelog()))
        w4.configure(state='disabled')
        w4.yview(END)

    def backward_and_update():  # Importing backward command and adding log update command to it to send to buttons
        backward()
        w4.configure(state='normal')
        w4.insert(tk.INSERT, str(updatelog()))
        w4.configure(state='disabled')
        w4.yview(END)

    def go_and_update():  # Importing go command and adding log update command to it to send to buttons
        go()
        w4.configure(state='normal')
        w4.insert(tk.INSERT, str(updatelog()))
        w4.configure(state='disabled')
        w4.yview(END)

    def stop_and_update():  # Importing stop command and adding log update command to it to send to buttons
        stop()
        w4.configure(state='normal')
        w4.insert(tk.INSERT, str(updatelog()))
        w4.configure(state='disabled')
        w4.yview(END)

    def update_overlay_frame():
        ret, frame = next(road_overlay_stream())
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # convert color from bgr to rgb
            img = Image.fromarray(frame) # turns the array into a usable frame
            imgtk = ImageTk.PhotoImage(image=img) # turns the frame into an image that can be displayed
            video.create_image(0, 0, image=imgtk, anchor=tk.NW)
            video.imgtk = imgtk
        ret2, frame2 = next(road_stream())
        if ret2:
            frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)  # convert color from bgr to rgb
            img2 = Image.fromarray(frame2) # turns the array into a usable frame
            imgtk2 = ImageTk.PhotoImage(image=img2) # turns the frame into an image that can be displayed
            video2.create_image(0, 0, image=imgtk2, anchor=tk.NW)
            video2.imgtk = imgtk2
        video.after(25, update_overlay_frame)  # call update frame again after 2 ms

    video = tk.Canvas(frame1, width=400, height=400, bg="gray")
    video.grid(row=0, column=0, rowspan=2, columnspan=2)

    video2 = tk.Canvas(frame3, width=400, height=400, bg="gray")
    video2.grid(row=0, column=0, rowspan=2, columnspan=2)

    update_overlay_frame()  # start updating the frame

    inner.mainloop()

# New update frame function found here: https://www.youtube.com/watch?v=s6O5hlZ0QM4