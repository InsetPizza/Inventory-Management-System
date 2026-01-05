from tkinter import *
from PIL import ImageTk, Image
import datetime
from tkinter import ttk
from tkcalendar import DateEntry
import pymysql
from tkinter import messagebox
from db import employee_form, connect_database
from supplier import supplier_form
from category import category_form
from product import product_form
from db import connect_database

#-------------------------------------------------
def tax_window():
    def save_tax():
        value=tax_count.get()
        cursor, connection = connect_database()
        if not connection or not cursor:
            return
        cursor.execute('USE inventory_system')
        cursor.execute('CREATE TABLE IF NOT EXISTS tax_table (id INT PRIMARY KEY, tax DECIMAL(5,2))')
        cursor.execute('SELECT id FROM tax_table WHERE id=1')
        if cursor.fetchone():
            cursor.execute('UPDATE tax_table SET tax = %s WHERE id=1', value)
        else:
            cursor.execute('INSERT INTO tax_table (id,tax) VALUES (1, %s)', value)

        connection.commit()
        messagebox.showinfo('Success', f'Tax has been set to {value} and saved successfully', parent=tax_root)


    tax_root=Toplevel()
    tax_root.title("Tax Calculator")
    tax_root.geometry("400x300")
    tax_root.grab_set()
    tax_percentage = Label(tax_root, text="Tax Percentage", font=("Arial", 12))
    tax_percentage.pack(pady=10)
    tax_count=Spinbox(tax_root, from_=0, to=100, font=("Arial", 12), width=20)
    tax_count.pack(pady=10)
    save_button = Button(tax_root, text='SAVE', font=('arial', 12, 'bold'), bg='sky blue', command= lambda: save_tax())
    save_button.pack(pady=10)

#----------------------------------
current_frame=None
def show_form(form_function):
    global current_frame
    if current_frame:
        current_frame.place_forget()
    current_frame= form_function(root)

#----------------------------------
def update_time():
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute('use inventory_system')
    cursor.execute('SELECT * FROM employee_data')
    emprecords = cursor.fetchall()
    totalemp_countLabel.config(text = len(emprecords))

    cursor.execute('SELECT * FROM supplier_data')
    suprecords = cursor.fetchall()
    totalsup_countLabel.config(text=len(suprecords))

    cursor.execute('SELECT * FROM category_data')
    catrecords = cursor.fetchall()
    totalcat_countLabel.config(text=len(catrecords))

    cursor.execute('SELECT * FROM product_data')
    prodrecords = cursor.fetchall()
    totalprod_countLabel.config(text=len(prodrecords))

    now = datetime.datetime.now()
    date_string = now.strftime("%b-%d-%Y")
    time_string = now.strftime("%H:%M:%S")

    full_text = f"Welcome Admin\t\t Date:{date_string}\t\t Time:{time_string}"
    subtitleLabel.config(text=full_text)
    subtitleLabel.after(1000, update_time)


# GUI Part
root = Tk()
root.state('zoomed')

bgimage = Image.open('bg.jpg')
bg = ImageTk.PhotoImage(file='bg.jpg')
bgLabel = Label(root, image=bg)
bgLabel.place(x=0, y=0)

toplogo = PhotoImage(file='toplogo.png')
titleLabel = Label(root, image=toplogo, compound=LEFT, text='    Inventory Management System',
                   font=('times new roman', 30, 'bold'), bg='blanched almond')
titleLabel.place(x=0, y=0)
titleLabel.pack(pady=10, fill='x')

logout_button = Button(root, text='Logout', font=('times new roman', 15, 'bold'))
logout_button.place(x=1350, y=15)

subtitleLabel = Label(root, text="", font=('times new roman', 15, 'bold'), bg='white smoke')
subtitleLabel.place(x=0, y=70, relwidth=1)

leftFrame = Frame(root)
leftFrame.place(x=0, y=98, width=300, height=700)

logoImage = PhotoImage(file='inventory.png')
imageLabel = Label(leftFrame, image=logoImage)
imageLabel.pack(pady=(10, 20))

menuLabel = Label(leftFrame, text='Menu', font=('times new roman', 24, 'bold'), bg='sky blue')
menuLabel.pack(fill='x')

employee_button = Button(leftFrame, text='Employee', font=('times new roman', 20, 'bold'), anchor='w', padx=50,
                         command=lambda: show_form(employee_form))
employee_button.pack(fill='x')

supplier_button = Button(leftFrame, text='Supplier', font=('times new roman', 20, 'bold'), anchor='w', padx=50,
                         command=lambda: show_form(supplier_form))
supplier_button.pack(fill='x')

category_button = Button(leftFrame, text='Category', font=('times new roman', 20, 'bold'), anchor='w', padx=50,
                         command = lambda: show_form(category_form))
category_button.pack(fill='x')

product_button = Button(leftFrame, text='Product', font=('times new roman', 20, 'bold'), anchor='w', padx=50,
                        command= lambda: show_form(product_form))
product_button.pack(fill='x')

sales_button = Button(leftFrame, text='Sales', font=('times new roman', 20, 'bold'), anchor='w', padx=50)
sales_button.pack(fill='x')

tax_button= Button(leftFrame, text='Tax', font=('times new roman', 20, 'bold'), anchor='w', padx=50, command=lambda: tax_window())
tax_button.pack(fill='x')

exit_button = Button(leftFrame, text='Exit', font=('times new roman', 20, 'bold'), anchor='w', padx=50)
exit_button.pack(fill='x')

emp_frame = Frame(root, bg='steel blue', bd=3, relief=RIDGE)
emp_frame.place(x=450, y=125, height=170, width=280)
totalempLabel = Label(emp_frame, text='Total Employees', bg='steel blue', fg='white',
                      font=('times new roman', 22, 'bold'))
totalempLabel.pack()
totalemp_countLabel = Label(emp_frame, text='0', bg='steel blue', fg='white', font=('times new roman', 30, 'bold'))
totalemp_countLabel.pack()

sup_frame = Frame(root, bg='medium sea green', bd=3, relief=RIDGE)
sup_frame.place(x=800, y=125, height=170, width=280)
totalsupLabel = Label(sup_frame, text='Total Suppliers', bg='medium sea green', fg='white',
                      font=('times new roman', 22, 'bold'))
totalsupLabel.pack()
totalsup_countLabel = Label(sup_frame, text='0', bg='medium sea green', fg='white',
                            font=('times new roman', 30, 'bold'))
totalsup_countLabel.pack()

cat_frame = Frame(root, bg='pale violet red', bd=3, relief=RIDGE)
cat_frame.place(x=450, y=310, height=170, width=280)
totalcatLabel = Label(cat_frame, text='Total Categories', bg='pale violet red', fg='white',
                      font=('times new roman', 22, 'bold'))
totalcatLabel.pack()
totalcat_countLabel = Label(cat_frame, text='0', bg='pale violet red', fg='white', font=('times new roman', 30, 'bold'))
totalcat_countLabel.pack()

prod_frame = Frame(root, bg='medium purple', bd=3, relief=RIDGE)
prod_frame.place(x=800, y=310, height=170, width=280)
totalprodLabel = Label(prod_frame, text='Total Products', bg='medium purple', fg='white',
                       font=('times new roman', 22, 'bold'))
totalprodLabel.pack()
totalprod_countLabel = Label(prod_frame, text='0', bg='medium purple', fg='white', font=('times new roman', 30, 'bold'))
totalprod_countLabel.pack()

sales_frame = Frame(root, bg='DarkOliveGreen3', bd=3, relief=RIDGE)
sales_frame.place(x=600, y=495, height=170, width=280)
totalsalesLabel = Label(sales_frame, text='Total Sales', bg='DarkOliveGreen3', fg='white',
                        font=('times new roman', 22, 'bold'))
totalsalesLabel.pack()
totalsales_countLabel = Label(sales_frame, text='0', bg='DarkOliveGreen3', fg='white',
                              font=('times new roman', 30, 'bold'))
totalsales_countLabel.pack()

update_time()
root.mainloop()
