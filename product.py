from tkinter import *
from tkinter import ttk
import pymysql
from tkinter import messagebox

import supplier
from db import connect_database


def treeview_data(treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute('use inventory_system')
    try:
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS product_data (id INT AUTO_INCREMENT PRIMARY KEY,'
            ' category VARCHAR(100), supplier VARCHAR(100), name VARCHAR(100), price DECIMAL(10,2),'
            ' discount FLOAT, discounted_price DECIMAL(10,2), quantity INT, status VARCHAR(10))')
        #cursor.execute('ALTER table product_data ADD COLUMN discount INT AFTER price ADD COLUMN discounted_price DECIMAL(10,2) AFTER discount')
        cursor.execute('SELECT * FROM product_data')
        records = cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()

#---------------------------------------------------------------------

def clear_fields(category_combobox, supplier_combobox, nameEntry,
                                                priceEntry,discount_spinbox, quantityEntry, status_combobox, treeview):
    treeview.selection_remove(treeview.selection())
    category_combobox.set('Select')
    supplier_combobox.set('Select')
    nameEntry.delete(0, END)
    priceEntry.delete(0, END)
    discount_spinbox.delete(0, END)
    discount_spinbox.insert(0,'0')
    quantityEntry.delete(0, END)
    status_combobox.set('Select Status')

#-----------------------------------------------------------------------------------------

def search_product(search_combobox, searchEntry, treeview):
    column = search_combobox.get()
    value = searchEntry.get()

    if column == 'Search Product':
        messagebox.showwarning('Warning', 'Please select a search option')
        return
    elif value == '':
        messagebox.showwarning('Warning', 'Please enter a value to search')
        return

    allowed_columns = ['Category', 'Supplier', 'Name', 'Status']
    if column not in allowed_columns:
        messagebox.showerror('Error', 'Invalid search field.')
        return

    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventory_system')
        query = f"SELECT * FROM product_data WHERE {column} LIKE %s"
        search_value = f'%{value}%'
        cursor.execute(query, (search_value,))
        records = cursor.fetchall()

        treeview.delete(*treeview.get_children())

        if records:
            for record in records:
                treeview.insert('', END, values=record)
        else:
            messagebox.showinfo('Info', 'No supplier found with that invoice number.')

    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()

#------------------------------------------------------------------------

def show_product(treeview, search_combobox, searchEntry):
    treeview_data(treeview)
    search_combobox.set('Search Product')
    searchEntry.delete(0, END)

#---------------------------------------------------------------------------------

def fetch_category(category_combobox, supplier_combobox):
    category_option=[]
    supplier_option = []
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute('use inventory_system')
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS category_data (id INT PRIMARY KEY, cat VARCHAR(100),'
        'description VARCHAR(1000))')
    cursor.execute('SELECT cat FROM category_data')
    cats=cursor.fetchall()
    if len(cats)>0:
        category_combobox.set('Select')
        for name in cats:
            category_option.append(name[0])
        category_combobox.config(values=category_option)
    else:
        category_combobox.set('Empty')

    cursor.execute(
        'CREATE TABLE IF NOT EXISTS supplier_data (invoice INT PRIMARY KEY, name VARCHAR(100), contact VARCHAR(100), description VARCHAR(1000))')
    cursor.execute('SELECT name FROM supplier_data')
    names=cursor.fetchall()
    if len(names)>0:
        supplier_combobox.set('Select')
        for name in names:
            supplier_option.append(name[0])
        supplier_combobox.config(values=supplier_option)
    else:
        supplier_combobox.set('Empty')


#------------------------------------------------------------------

def add_product(category, supplier, name, price, discount, quantity, status, treeview):
    if category=='Empty':
        messagebox.showerror('Error', 'Please add a category first.')
    elif supplier=='Empty':
        messagebox.showerror('Error', 'Please add a supplier first.')
    elif (category == 'Select' or supplier == 'Select' or name == '' or price == ''
          or quantity == '' or status=='Select Status'):
        messagebox.showerror('Error', 'Please fill all fields')
    else:
        try:
            price_val = float(price)
            discount_val = float(discount)
            quantity_val = int(quantity)
        except ValueError:
            messagebox.showerror('Error', 'Price, Discount, and Quantity must be valid numbers.')
            return

        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        cursor.execute('use inventory_system')
        try:
            cursor.execute(
                'CREATE TABLE IF NOT EXISTS product_data (id INT AUTO_INCREMENT PRIMARY KEY,'
                ' category VARCHAR(100), supplier VARCHAR(100), name VARCHAR(100), price DECIMAL(10,2), '
                'discount FLOAT, discounted_price DECIMAL(10,2), quantity INT, status VARCHAR(10))')
            # cursor.execute(
            #     'ALTER table product_data ADD COLUMN IF NOT EXISTS discount INT AFTER price, ADD COLUMN IF NOT EXISTS discounted_price DECIMAL(10,2) AFTER discount')
            cursor.execute('SELECT * FROM product_data WHERE category=%s AND supplier=%s AND name=%s', (category, supplier, name))
            if cursor.fetchone():
                messagebox.showerror('Error', 'Product already exists')
            else:
                discounted_price = round(price_val*(1- discount_val/100), 2 )
                cursor.execute(
                    'INSERT INTO product_data (category, supplier, name, price, discount, discounted_price,  quantity, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                    (category, supplier, name, price_val, discount_val, discounted_price, quantity_val, status))
                connection.commit()
                messagebox.showinfo('Success', 'Data has been added')
                treeview_data(treeview)
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()


#------------------------------------------------------------------

def delete_product(treeview, category_combobox, supplier_combobox, nameEntry,
                                                priceEntry, discount_spinbox, quantityEntry, status_combobox):
    index = treeview.selection()
    dict = treeview.item(index)
    content = dict['values']
    id = content[0]
    if not index:
        messagebox.showerror('Error', 'Please select a Category')
        return
    ans=messagebox.askyesno('Delete', 'Do you really want to delete this product?')
    if ans:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('use inventory_system')
            cursor.execute('DELETE FROM product_data WHERE id=%s', id)
            connection.commit()
            treeview_data(treeview)
            messagebox.showinfo('Info', 'Product Deleted')
            clear_fields(category_combobox, supplier_combobox, nameEntry,
                                                priceEntry, discount_spinbox, quantityEntry, status_combobox, treeview)
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()

#---------------------------------------------------------------------

def update_product(category, supplier, name, price, discount, quantity, status, treeview):
    index = treeview.selection()
    dict=treeview.item(index)
    content=dict['values']
    id=content[0]
    if not index:
        messagebox.showerror('Error', 'Please select a category')
        return

    try:
        price_val = float(price)
        discount_val = float(discount)
        quantity_val = int(quantity)
    except ValueError:
        messagebox.showerror('Error', 'Price, Discount, and Quantity must be valid numbers.')
        return
    discounted_price = round(price_val * (1 - discount_val / 100), 2)

    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute('use inventory_system')
    cursor.execute('SELECT * FROM product_data WHERE id = %s', (id,))
    current_data = cursor.fetchone()
    current_data = current_data[1:]
    current_data = list(current_data)
    current_data[3]= str(current_data[3])
    current_data=tuple(current_data)
    quantity=int(quantity)
    new_data = (category, supplier, name, price, quantity, status)

    if current_data == new_data:
        messagebox.showinfo('Info', 'No changes made')
        return
    try:
        cursor.execute('UPDATE product_data SET category=%s, supplier=%s, name=%s, price=%s, discount=%s, discounted_price=%s, quantity=%s, status=%s WHERE id=%s',
                       (category, supplier, name, price_val, discount_val, discounted_price, quantity_val, status, id))
        connection.commit()
        messagebox.showinfo('Success', 'ID updated')
        treeview_data(treeview)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()


# -------------------------------------------------------------------------------------

def select_data(event, category_combobox, supplier_combobox, nameEntry,
                priceEntry, discount_spinbox, quantityEntry, status_combobox, treeview):
    index = treeview.selection()
    if not index:
        return
    item = treeview.item(index)
    content = item['values']

    nameEntry.delete(0, END)
    priceEntry.delete(0, END)
    discount_spinbox.delete(0, END)
    quantityEntry.delete(0, END)

    category_combobox.set(content[1])
    supplier_combobox.set(content[2])
    nameEntry.insert(0, content[3])
    priceEntry.insert(0, content[4])
    discount_spinbox.insert(0, int(float(content[5])))
    quantityEntry.insert(0, content[7])
    status_combobox.set(content[8])

#-----------------------------------------------------------------------

def product_form(root):
    global back_image, treeview;
    product_frame = Frame(root, bg='white')
    product_frame.place(x=300, y=100, width=1230, height=750)
    back_image = PhotoImage(file='back.png')
    back_button = Button(product_frame, image=back_image, bg='white', bd=0, cursor='hand2',
                         command=lambda: product_frame.place_forget())
    back_button.place(x=10, y=30)

    left_frame = Frame(product_frame, bg='white', bd=2, relief=RIDGE, padx=20)
    left_frame.place(x=20, y=70)

    headingLabel = Label(left_frame, text="Manage Product Details", font=('times new roman', 16, 'bold'),
                         bg='sky blue')
    headingLabel.grid(row=0, column=0, columnspan=2, sticky='we')

    category_label = Label(left_frame, text='Category', font=('times new roman', 14, 'bold'), bg='white')
    category_label.grid(row=1, column=0, padx=(20, 40), pady=15, sticky='w')
    category_combobox = ttk.Combobox(left_frame, font=('times new roman', 14, 'bold'), width = 18, state='readonly')
    category_combobox.grid(row=1, column=1)
    category_combobox.set('Empty')

    supplier_label = Label(left_frame, text='Supplier', font=('times new roman', 14, 'bold'), bg='white')
    supplier_label.grid(row=2, column=0, padx=(20, 40), pady=15, sticky='w')
    supplier_combobox = ttk.Combobox(left_frame, font=('times new roman', 14, 'bold'), width=18, state='readonly')
    supplier_combobox.grid(row=2, column=1)
    supplier_combobox.set('Empty')

    name_label = Label(left_frame, text='Name', font=('times new roman', 14, 'bold'), bg='white')
    name_label.grid(row=3, column=0, padx=(20, 40), pady=15, sticky='w')
    nameEntry = Entry(left_frame, bg='lightyellow', font=('times new roman', 14, 'bold'), width=20)
    nameEntry.grid(row=3, column=1)

    price_label = Label(left_frame, text='Price', font=('times new roman', 14, 'bold'), bg='white')
    price_label.grid(row=4, column=0, padx=(20, 40), pady=15, sticky='w')
    priceEntry = Entry(left_frame, bg='lightyellow', font=('times new roman', 14, 'bold'), width=20)
    priceEntry.grid(row=4, column=1)

    discount_label = Label(left_frame, text='Discount(%)', font=('times new roman', 14, 'bold'), bg='white')
    discount_label.grid(row=5, column=0, padx=(20, 40), pady=15, sticky='w')
    discount_spinbox = Spinbox(left_frame, from_=0, to=100, font=('times new roman', 14, 'bold'), width=20)
    discount_spinbox.grid(row=5, column=1)

    quantity_label = Label(left_frame, text='Quantity', font=('times new roman', 14, 'bold'), bg='white')
    quantity_label.grid(row=6, column=0, padx=(20, 40), pady=15, sticky='w')
    quantityEntry = Entry(left_frame, bg='lightyellow', font=('times new roman', 14, 'bold'), width=20)
    quantityEntry.grid(row=6, column=1)

    status_label = Label(left_frame, text='Status', font=('times new roman', 14, 'bold'), bg='white')
    status_label.grid(row=7, column=0, padx=(20, 40), pady=15, sticky='w')
    status_combobox = ttk.Combobox(left_frame, values=('Active', 'Inactive'), font=('times new roman', 14, 'bold'), width=18, state='readonly')
    status_combobox.grid(row=7, column=1)
    status_combobox.set('Select Status')

    button_frame = Frame(left_frame, bg='white')
    button_frame.grid(row=8, columnspan=2, pady=20)

    add_button = Button(button_frame, text='ADD', font=('times new roman', 14), bg='sky blue', width=10,
                        cursor='hand2', command=lambda: add_product(category_combobox.get(), supplier_combobox.get(), nameEntry.get(),
                                                                    priceEntry.get(), discount_spinbox.get(), quantityEntry.get(), status_combobox.get(), treeview))
    add_button.grid(row=0, column=1, padx=20, pady=30)

    update_button = Button(button_frame, text='UPDATE', font=('times new roman', 14), bg='sky blue', width=10,
                           cursor='hand2', command=lambda: update_product(category_combobox.get(), supplier_combobox.get(),nameEntry.get(),
                                                                    priceEntry.get(), discount_spinbox.get(), quantityEntry.get(), status_combobox.get(), treeview))
    update_button.grid(row=0, column=2, pady=30)

    delete_button = Button(button_frame, text='DELETE', font=('times new roman', 14), bg='sky blue', width=10,
                           cursor='hand2', command= lambda: delete_product(treeview, category_combobox, supplier_combobox, nameEntry,
                                                priceEntry, discount_spinbox, quantityEntry, status_combobox))
    delete_button.grid(row=0, column=3, padx=20, pady=30)

    clear_button = Button(button_frame, text='CLEAR', font=('times new roman', 14), bg='sky blue', width=10,
                          cursor='hand2',
                          command=lambda: clear_fields(category_combobox, supplier_combobox, nameEntry,
                                                priceEntry, discount_spinbox, quantityEntry, status_combobox, treeview))
    clear_button.grid(row=0, column=4, pady=30)

    right_frame=LabelFrame(product_frame, bg='white', text='Search Product', font=('times new roman', 14))
    right_frame.place(x=600, y=60)

    search_combobox=ttk.Combobox(right_frame, values=('Category', 'Supplier', 'Name', 'Status'), state='readonly')
    search_combobox.grid(row=0, column=0, padx=(10, 20), pady=15, sticky='w')
    search_combobox.set('Search Product')
    searchEntry = Entry(right_frame, bg='lightyellow', font=('times new roman', 14, 'bold'), width=10)
    searchEntry.grid(row=0, column=1)

    search_button = Button(right_frame, text='SEARCH', font=('times new roman', 14), bg='sky blue', width=10,
                           cursor='hand2', command= lambda: search_product(search_combobox, searchEntry, treeview))
    search_button.grid(row=0, column=2, padx=20, pady=30)

    show_button = Button(right_frame, text='SHOW ALL', font=('times new roman', 14), bg='sky blue', width=10,
                           cursor='hand2', command=lambda: show_product(treeview, search_combobox, searchEntry))
    show_button.grid(row=0, column=3, padx=20, pady=30)

    treeview_frame = Frame(product_frame, bg='white')
    treeview_frame.place(x=600, y=200, height=450, width=600)

    scrolly = Scrollbar(treeview_frame, orient=VERTICAL)
    scrollx = Scrollbar(treeview_frame, orient=HORIZONTAL)
    treeview = ttk.Treeview(treeview_frame, columns=('id', 'category', 'supplier', 'name', 'price', 'discount', 'discounted_price', 'quantity', 'status'), show='headings',
                            yscrollcommand=scrolly.set,
                            xscrollcommand=scrollx.set)
    scrolly.pack(side=RIGHT, fill='y')
    scrollx.pack(side=BOTTOM, fill='x')
    scrolly.config(command=treeview.yview)
    scrollx.config(command=treeview.xview)
    treeview.pack(fill=BOTH, expand=1)
    treeview.heading('id', text='ID')
    treeview.heading('category', text='Category')
    treeview.heading('supplier', text='Supplier')
    treeview.heading('name', text='Product Name')
    treeview.heading('price', text='Price')
    treeview.heading('discount', text='Discount')
    treeview.heading('discounted_price', text='Discounted Price')
    treeview.heading('quantity', text='Quantity')
    treeview.heading('status', text='Status')

    treeview.column('id', width=50)
    treeview.column('category', width=100)
    treeview.column('supplier', width=100)
    treeview.column('name', width=100)
    treeview.column('price', width=50)
    treeview.column('discount', width=50)
    treeview.column('discounted_price', width=80)
    treeview.column('quantity', width=80)
    treeview.column('status', width=100)

    fetch_category(category_combobox, supplier_combobox)

    treeview_data(treeview)
    treeview.bind('<Double-1>',
                  lambda event: select_data(event, category_combobox, supplier_combobox,
                                        nameEntry, priceEntry, discount_spinbox, quantityEntry,
                                        status_combobox, treeview))

    return product_frame