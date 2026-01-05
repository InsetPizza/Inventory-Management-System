from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image
from db import connect_database

def login():
    if username_entry.get()=='' or password_entry.get()=='':
        messagebox.showerror('Error', 'Please fill out the fields')
    elif username_entry.get()=='Shailja' and password_entry.get()=='1234':
        messagebox.showinfo('Success', 'Welcome')
    else:
        messagebox.showerror('Error', 'Please fill out correct details')

#--------------------------------------------------------------------------

def signin(username_entry, password_entry, usertype_combobox):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute('use inventory_system')
    try:
        cursor.execute('CREATE TABLE IF NOT EXISTS login_data (username PRIMARY VARCHAR(100), password VARCHAR(100), usertype VARCHAR(100))')
        sql= 'insert into login_data(username, password, usertype) values(%s, %s, %s))'
        values = (username_entry.get(), password_entry.get(), usertype_combobox.get())
        cursor.execute(sql, values)
        connection.commit()
        messagebox.showinfo('Success', 'Please go back to login page')

    except pymysql.Error as e:
        messagebox.showerror('Error', f'Error due to: {e}')
        connection.rollback()
        connection.close()

#-----------------------------------------------------------------------------

root = Tk()

root.geometry('1920x1080+0+0')

image_file= Image.open('bg.jpg')

#conver image to tkinter compatible photoimage
background_image = ImageTk.PhotoImage(file='bg.jpg')

bgLabel = Label(root, image = background_image) #we can add bg image to this label
bgLabel.place(x=0, y=0)

inventory_frame = Frame(root, bg='sky blue')
inventory_frame.place(x=0, y=0)
inventory_label = Label(inventory_frame, text='Inventory Management System', font = ('times new roman', 25, 'bold'), bg='sky blue')
inventory_label.pack(padx=550, pady=20)

#----------------
select_login = Frame(root, bg='sky blue')
select_login.place(x=590, y=160)
#-----------------------------------

login_frame = Frame(root, bg='white')
login_frame.place(x=590, y=160)

logo_image = PhotoImage(file = 'user.png')
logoLabel = Label(login_frame, image = logo_image, bg='white')
logoLabel.grid(row=0, column=0, columnspan=2, pady =10)

username_image = PhotoImage(file = 'user2.png')
username_label = Label(login_frame, image = username_image, text= 'Username', compound=LEFT
                       , font = ('times new roman', 15, 'bold'), bg='white')
username_label.grid(row=1, column=0, pady = 10, padx = 20)

username_entry=Entry(login_frame, font = ('times new roman', 15, 'bold'), bd=5)
username_entry.grid(row=1, column=1, pady = 10, padx = 20)

password_image = PhotoImage(file = 'lock.png')
password_label = Label(login_frame, image = password_image, text= 'Password', compound=LEFT
                       , font = ('times new roman', 15, 'bold'), bg='white')
password_label.grid(row=2, column=0, pady = 10, padx = 20)

password_entry=Entry(login_frame, font = ('times new roman', 15, 'bold'), bd=5)
password_entry.grid(row=2, column=1, pady = 10, padx = 20)

usertype_label = Label(select_login, font = ('times new roman', 15, 'bold'), bg='white', text='User-Type')
usertype_label.grid(row=3, column=0, pady = 10, padx = 20)
usertype_combobox= ttk.Combobox(select_login, values=('Manager', 'Customer'), font = ('times new roman', 15, 'bold'))
usertype_combobox.grid(row=3, column=1, pady = 10, padx = 20)

signin_button = Button(login_frame, font=('times new roman', 15, 'bold'), command= lambda: signin(username_entry.get(), password_entry.get(), usertype_combobox.get()))
signin_button.grid(row=3, column=0)

login_inn_button = Button(login_frame, font=('times new roman', 15, 'bold'))
login_inn_button.grid(row=3, column=1)

login_button= Button(login_frame, text = 'Login', font = ('times new roman', 15, 'bold'), cursor='hand2', command=lambda: login())
login_button.grid(row=3, column=1, pady = 10, padx = 20)
root.mainloop()