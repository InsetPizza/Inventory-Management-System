from tkinter import *
import datetime
from tkinter import ttk
from tkcalendar import DateEntry
import pymysql
from tkinter import messagebox
from db import connect_database
from product import product_form

def clear(invoiceEntry, nameEntry, contactEntry, decriptionText, treeview):
    invoiceEntry.delete(0, END)
    nameEntry.delete(0, END)
    contactEntry.delete(0, END)
    decriptionText.delete(1.0, END)
    treeview.selection_remove(treeview.selection())

#----------------------------------------------------------------------------------

def search_supplier(search_value, treeview):
    if search_value == '':
        messagebox.showerror('Error', 'Invoice cannot be empty')
        return

    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    try:
        cursor.execute('use inventory_system')
        cursor.execute('SELECT * FROM supplier_data WHERE invoice=%s', (search_value,))
        rrecord = cursor.fetchone()

        treeview.delete(*treeview.get_children())

        if rrecord:
            treeview.insert('', END, values=rrecord)
        else:
            messagebox.showinfo('Info', 'No supplier found with that invoice number.')

    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()

#------------------------------------------------------------------------

def show_all(treeview, numEntry):
    treeview_data(treeview)
    numEntry.delete(0, END)

#-------------------------------------------------------------------

def delete_supplier(invoice, treeview):
    index = treeview.selection()
    if not index:
        messagebox.showerror('Error', 'Please select a Supplier')
        return
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventory_system')
        cursor.execute('DELETE FROM supplier_data WHERE invoice=%s', invoice)
        connection.commit()
        treeview_data(treeview)
        messagebox.showinfo('Info', 'Supplier Deleted')
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()

#---------------------------------------------------------------------

def update_supplier(invoice, name, contact, description, treeview):
    index = treeview.selection()
    if not index:
        messagebox.showerror('Error', 'Please select a Supplier')
        return
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute('use inventory_system')
    cursor.execute('SELECT * FROM supplier_data WHERE invoice = %s', (invoice,))
    current_data = cursor.fetchone()
    current_data = current_data[1:]
    new_data = (name, contact, description)

    cursor.execute('SELECT name FROM supplier_data WHERE invoice = %s', (invoice,))
    old_name = cursor.fetchone()[0]
    new_name= name

    if current_data == new_data:
        messagebox.showinfo('Info', 'No changes made')
        return
    try:
        cursor.execute('UPDATE supplier_data SET name=%s, contact=%s, description=%s WHERE invoice=%s',
                       (name, contact, description, invoice))
        if old_name != new_name:
            cursor.execute('UPDATE product_data SET supplier=%s WHERE supplier=%s',
                           (new_name, old_name))
        connection.commit()
        messagebox.showinfo('Success', 'Invoice updated')
        treeview_data(treeview)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()


# -------------------------------------------------------------------------------------

def select_data(event, invoiceEntry, nameEntry, contactEntry, decriptionText, treeview):
    index = treeview.selection()
    content = treeview.item(index)
    actual_content = content['values']

    invoiceEntry.delete(0, END)
    nameEntry.delete(0, END)
    contactEntry.delete(0, END)
    decriptionText.delete(1.0, END)

    invoiceEntry.insert(0, actual_content[0])
    nameEntry.insert(0, actual_content[1])
    contactEntry.insert(0, actual_content[2])
    decriptionText.insert(1.0, actual_content[3])


# ------------------------------------------------------------------------------------

def treeview_data(treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute('use inventory_system')
    try:
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS supplier_data (invoice INT PRIMARY KEY, name VARCHAR(100),'
            ' contact VARCHAR(100), description VARCHAR(1000))')
        cursor.execute('SELECT * FROM supplier_data')
        records = cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()


# ----------------------------------------------------------------------------------------

def add_supplier(invoice, name, contact, description, treeview):
    if invoice == '' or name == '' or contact == '' or description == '':
        messagebox.showerror('Error', 'Please fill all fields')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        cursor.execute('use inventory_system')
        try:
            cursor.execute(
                'CREATE TABLE IF NOT EXISTS supplier_data (invoice INT PRIMARY KEY, name VARCHAR(100), contact VARCHAR(100), description VARCHAR(1000))')
            cursor.execute('SELECT * FROM supplier_data WHERE invoice=%s', invoice)
            if cursor.fetchone():
                messagebox.showerror('Error', 'Id already exists')
            else:
                cursor.execute('INSERT INTO supplier_data VALUES (%s, %s, %s, %s)',
                               (invoice, name, contact, description))
                connection.commit()
                messagebox.showinfo('Success', 'Data has been added')
                treeview_data(treeview)
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()


# ------------------------------------------------------------------------------

def supplier_form(root):
    global back_image, treeview;
    supplier_frame = Frame(root, bg='white')
    supplier_frame.place(x=300, y=100, width=1230, height=750)
    headingLabel = Label(supplier_frame, text="Manage Supplier Details", font=('times new roman', 16, 'bold'),
                         bg='sky blue')
    headingLabel.place(x=0, y=0, relwidth=1)
    back_image = PhotoImage(file='back.png')
    back_button = Button(supplier_frame, image=back_image, bg='white', bd=0, cursor='hand2',
                         command=lambda: supplier_frame.place_forget())
    back_button.place(x=10, y=30)

    left_frame = Frame(supplier_frame, bg='white')
    left_frame.place(x=10, y=110, width=600, height=625)

    invoice_label = Label(left_frame, text='Invoice No.', font=('times new roman', 14, 'bold'), bg='white')
    invoice_label.grid(row=0, column=0, padx=(20, 40), pady=15, sticky='w')
    invoiceEntry = Entry(left_frame, bg='lightyellow', font=('times new roman', 14, 'bold'), width=30)
    invoiceEntry.grid(row=0, column=1)

    name_label = Label(left_frame, text='Supplier Name', font=('times new roman', 14, 'bold'), bg='white')
    name_label.grid(row=1, column=0, padx=(20, 40), pady=15, sticky='w')
    nameEntry = Entry(left_frame, bg='lightyellow', font=('times new roman', 14, 'bold'), width=30)
    nameEntry.grid(row=1, column=1)

    contact_label = Label(left_frame, text='Contact', font=('times new roman', 14, 'bold'), bg='white')
    contact_label.grid(row=2, column=0, padx=(20, 40), pady=15, sticky='w')
    contactEntry = Entry(left_frame, bg='lightyellow', font=('times new roman', 14, 'bold'), width=30)
    contactEntry.grid(row=2, column=1)

    description_label = Label(left_frame, text='Description', font=('times new roman', 14, 'bold'), bg='white')
    description_label.grid(row=3, column=0, padx=(20, 40), sticky='nw', pady=25)
    descriptionText = Text(left_frame, bg='lightyellow', font=('times new roman', 14, 'bold'), width=30, height=6, bd=2)
    descriptionText.grid(row=3, column=1, pady=25)

    button_frame = Frame(left_frame, bg='white')
    button_frame.grid(row=4, column=0, columnspan=4)

    add_button = Button(button_frame, text='ADD', font=('times new roman', 14), bg='sky blue', width=10,
                        cursor='hand2', command=lambda: add_supplier(invoiceEntry.get(), nameEntry.get(),
                                                                     contactEntry.get(),
                                                                     descriptionText.get(1.0, END), treeview))
    add_button.grid(row=0, column=0, padx=20, pady=10)

    update_button = Button(button_frame, text='UPDATE', font=('times new roman', 14), bg='sky blue', width=10,
                           cursor='hand2', command=lambda: update_supplier(invoiceEntry.get(), nameEntry.get(),
                                                                           contactEntry.get(),
                                                                           descriptionText.get(1.0, END), treeview))
    update_button.grid(row=0, column=1, pady=10)

    delete_button = Button(button_frame, text='DELETE', font=('times new roman', 14), bg='sky blue', width=10,
                           cursor='hand2', command=lambda: delete_supplier(invoiceEntry.get(), treeview))
    delete_button.grid(row=0, column=2, padx=20, pady=10)

    clear_button = Button(button_frame, text='CLEAR', font=('times new roman', 14), bg='sky blue', width=10,
                          cursor='hand2', command= lambda: clear(invoiceEntry, nameEntry, contactEntry, descriptionText, treeview))
    clear_button.grid(row=0, column=3, pady=10)

    right_frame = Frame(supplier_frame, bg='white')
    right_frame.place(x=625, y=95, width=550, height=500)

    search_frame = Frame(right_frame, bg='white')
    search_frame.pack(pady=(0, 10))

    num_label = Label(search_frame, text='Invoice No.', font=('times new roman', 14, 'bold'), bg='white')
    num_label.grid(row=0, column=0, padx=(0, 20), pady=10, sticky='w')
    numEntry = Entry(search_frame, bg='lightyellow', font=('times new roman', 14, 'bold'), width=10)
    numEntry.grid(row=0, column=1)

    search_button = Button(search_frame, text='SEARCH', font=('times new roman', 14), bg='sky blue', width=10,
                           cursor='hand2', command= lambda: search_supplier(numEntry.get(), treeview))
    search_button.grid(row=0, column=2, padx=10, pady=10)

    show_button = Button(search_frame, text='SHOW ALL', font=('times new roman', 14), bg='sky blue', width=10,
                         cursor='hand2', command = lambda: show_all(treeview, numEntry.get()))
    show_button.grid(row=0, column=3, pady=10)

    scrolly = Scrollbar(right_frame, orient=VERTICAL)
    scrollx = Scrollbar(right_frame, orient=HORIZONTAL)
    treeview = ttk.Treeview(right_frame, columns=('invoice', 'name', 'contact', 'description'), show='headings',
                            yscrollcommand=scrolly.set,
                            xscrollcommand=scrollx.set)
    scrolly.pack(side=RIGHT, fill='y')
    scrollx.pack(side=BOTTOM, fill='x')
    scrolly.config(command=treeview.yview)
    scrollx.config(command=treeview.xview)
    treeview.pack(fill=BOTH, expand=1)
    treeview.heading('invoice', text='Invoice Id')
    treeview.heading('name', text='Name')
    treeview.heading('contact', text='Contact')
    treeview.heading('description', text='Description')

    treeview.column('invoice', width=80)
    treeview.column('name', width=160)
    treeview.column('contact', width=120)
    treeview.column('description', width=300)

    treeview_data(treeview)
    treeview.bind('<Double-1>',
                  lambda event: select_data(event, invoiceEntry, nameEntry, contactEntry, descriptionText, treeview))
    return supplier_frame