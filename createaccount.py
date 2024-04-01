import tkinter as tk  # Importing UI library for python, tkinter, allowing to make buttons and text labels
from tkinter import ttk  # Importing specific part of tkinter
import sqlite3  # Importing sqlite3 which allows SQL queries to be called in python
import random  # Importing random library, which allows for random values to be generated
from tkinter import *  # Importing everything in tkinter
from tkinter import messagebox  # Importing messagebox from tkinter, allowing for message box pop-ups
import os  # Importing file managing library, which allows for editing and reading other files

db = sqlite3.connect('database.db')  # Connecting queries to file 'database.db'
cursor = db.cursor()  # Setting up database query-er

try:  # Testing to see if file exists
    if os.path.exists("database.db"):
        pass  # If it does, pass
except:  # If it doesn't create a file called database.db
    os.mknod("database.db")

try:  # Testing to see if 'id' table exists
    cursor.execute("SELECT id FROM database")
except:  # If  not, then create one with the arguments of id, firstname, lastname, username, and password
    cursor.execute("CREATE TABLE database (id, fn, ln, username, password)")


# Checks if username already exists and if not, creates a new account
def create(fn, ln, username, password):  # Function for create account
    cursor.execute(f"SELECT username FROM database WHERE username = '{username}'")  # Finding username in SQL table
    un = cursor.fetchone()  # Setting of query-er
    if un:  # If username already exists, tell user to create a new username
        messagebox.showinfo("Pick Something Else", "Username Already Exists")
    else:  # If it doesnt already exist, let is slide and generate a unique id
        randy = random.randint(100000, 999999)  # generating number between 100000 and 999999
        cursor.execute(f"SELECT id FROM database WHERE id = '{randy}'")
        inty = cursor.fetchone()
        while inty:  # Setting ID value of username to newly generated id
            randy = random.randint(100000, 999999)
            cursor.execute(f"SELECT id FROM database WHERE id = '{randy}'")
            inty = cursor.fetchone()

        # Inserting all new values into SQL database
        cursor.execute(
            f"INSERT INTO database VALUES ('{randy}', '{fn}', '{ln}', '{username}', '{password}')"
        )
        cursor.close()  # Closing query-er
        db.commit()  # Commiting changes

        messagebox.showinfo("Your account was created",
                            "You can sign in now!")  # Pop-up letting user know account has been created

# Makes the Create Window
def cw():
    root = Tk()  # Creating window
    root.geometry("500x500")  # Setting window to 500x500 pixels
    root.title("Create Account")  # Naming window "Create Account"

    e1 = StringVar()  # Creating textboxes
    e2 = StringVar()
    e3 = StringVar()
    e4 = StringVar()

    fn = Label(root, text="First name: ")  # Label for box
    fn.grid(row=0, column=0)  # Position for box
    enterfn = Entry(root, textvariable=e1)  # Text box setup
    enterfn.grid(row=0, column=1)  # Text box position

    ln = Label(root, text="Last name: ")  # Same setup as first box
    ln.grid(row=1, column=0)
    enterln = Entry(root, textvariable=e2)
    enterln.grid(row=1, column=1)

    user = Label(root, text="Username: ")  # Same setup as first box
    user.grid(row=2, column=0)
    enteruser = Entry(root, textvariable=e3)
    enteruser.grid(row=2, column=1)

    password = Label(root, text="Password: ")  # Same setup as first box
    password.grid(row=3, column=0)
    enterpass = Entry(root, textvariable=e4,show="\u00B7")  # Except this eplaces characters input into the texbox with "\u00B7" which is unicode for a bullet point, masking password
    enterpass.grid(row=3, column=1)

    create_button = Button(root, text="Create account",command=lambda: create(enterfn.get(), enterln.get(), enteruser.get(),enterpass.get()))  # Making create button and setting it to run the create account function on press

    create_button.grid(row=4, column=0)  # Create button position
