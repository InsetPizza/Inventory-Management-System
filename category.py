from tkinter import *
from tkinter import ttk
import pymysql
from tkinter import messagebox
from db import connect_database


def treeview_data(treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute('use inventory_system')
    try:
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS category_data (id INT PRIMARY KEY, cat VARCHAR(100),'
            'description VARCHAR(1000))')
        cursor.execute('SELECT * FROM category_data')
        records = cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()
#------------------------------------------------------------------------------------

def clear(idEntry, catEntry, decriptionText, treeview):
    idEntry.delete(0, END)
    catEntry.delete(0, END)
    decriptionText.delete(1.0, END)
    treeview.selection_remove(treeview.selection())

#------------------------------------------------------------------

def add_category(id, cat, description, treeview):
    if id == '' or cat == '' or description == '':
        messagebox.showerror('Error', 'Please fill all fields')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        cursor.execute('use inventory_system')
        try:
            cursor.execute(
                'CREATE TABLE IF NOT EXISTS category_data (id INT PRIMARY KEY, cat VARCHAR(100), description VARCHAR(1000))')
            cursor.execute('SELECT * FROM category_data WHERE id=%s', id)
            if cursor.fetchone():
                messagebox.showerror('Error', 'Id already exists')
            else:
                cursor.execute('INSERT INTO category_data VALUES (%s, %s, %s)',
                               (id, cat, description))
                connection.commit()
                messagebox.showinfo('Success', 'Data has been added')
                treeview_data(treeview)
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()


#------------------------------------------------------------------

def delete_category(id, treeview):
    index = treeview.selection()
    if not index:
        messagebox.showerror('Error', 'Please select a Category')
        return
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventory_system')
        cursor.execute('DELETE FROM category_data WHERE id=%s', id)
        connection.commit()
        treeview_data(treeview)
        messagebox.showinfo('Info', 'Category Deleted')
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()

#---------------------------------------------------------------------

def update_category(id, cat, description, treeview):
    index = treeview.selection()
    if not index:
        messagebox.showerror('Error', 'Please select a category')
        return
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute('use inventory_system')
    cursor.execute('SELECT * FROM category_data WHERE id = %s', (id,))
    current_data = cursor.fetchone()
    current_data = current_data[1:]
    new_data = (cat, description)

    if current_data == new_data:
        messagebox.showinfo('Info', 'No changes made')
        return
    try:
        cursor.execute('UPDATE category_data SET cat=%s, description=%s WHERE id=%s',
                       (cat, description, id))
        connection.commit()
        messagebox.showinfo('Success', 'ID updated')
        treeview_data(treeview)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()


# -------------------------------------------------------------------------------------

def select_data(event, idEntry, catEntry, decriptionText, treeview):
    index = treeview.selection()
    content = treeview.item(index)
    actual_content = content['values']

    idEntry.delete(0, END)
    catEntry.delete(0, END)
    decriptionText.delete(1.0, END)

    idEntry.insert(0, actual_content[0])
    catEntry.insert(0, actual_content[1])
    decriptionText.insert(1.0, actual_content[2])

#-----------------------------------------------------------------------

def category_form(root):
    global back_image, treeview;
    category_frame = Frame(root, bg='white')
    category_frame.place(x=300, y=100, width=1230, height=750)
    headingLabel = Label(category_frame, text="Manage Category Details", font=('times new roman', 16, 'bold'),
                         bg='sky blue')
    headingLabel.place(x=0, y=0, relwidth=1)
    back_image = PhotoImage(file='back.png')
    back_button = Button(category_frame, image=back_image, bg='white', bd=0, cursor='hand2',
                         command=lambda: category_frame.place_forget())
    back_button.place(x=10, y=30)

    logo = PhotoImage(file='shopping-bag.png')
    label= Label(category_frame, image=logo, bg='white')
    label.image= logo
    label.place(x=30, y=100)

    details_frame = Frame(category_frame, bg='white')
    details_frame.place(x=600, y=60)

    id_label = Label(details_frame, text='ID', font=('times new roman', 14, 'bold'), bg='white')
    id_label.grid(row=0, column=0, padx=(20, 40), pady=15, sticky='w')
    idEntry = Entry(details_frame, bg='lightyellow', font=('times new roman', 14, 'bold'), width=30)
    idEntry.grid(row=0, column=1)

    cat_label = Label(details_frame, text='Category', font=('times new roman', 14, 'bold'), bg='white')
    cat_label.grid(row=1, column=0, padx=(20, 40), pady=15, sticky='w')
    catEntry = Entry(details_frame, bg='lightyellow', font=('times new roman', 14, 'bold'), width=30)
    catEntry.grid(row=1, column=1)

    description_label = Label(details_frame, text='Description', font=('times new roman', 14, 'bold'), bg='white')
    description_label.grid(row=2, column=0, padx=(20, 40), sticky='nw', pady=25)
    descriptionText = Text(details_frame, bg='lightyellow', font=('times new roman', 14, 'bold'), width=30, height=6, bd=2)
    descriptionText.grid(row=2, column=1, pady=25)

    button_frame = Frame(category_frame, bg='white')
    button_frame.place(x=600, y=280)

    add_button = Button(button_frame, text='ADD', font=('times new roman', 14), bg='sky blue', width=10,
                        cursor='hand2', command=lambda: add_category(idEntry.get(), catEntry.get(),
                                                                     descriptionText.get(1.0, END), treeview))
    add_button.grid(row=0, column=0, padx=20, pady=30)

    update_button = Button(button_frame, text='UPDATE', font=('times new roman', 14), bg='sky blue', width=10,
                           cursor='hand2', command=lambda: update_category(idEntry.get(), catEntry.get(),
                                                                           descriptionText.get(1.0, END), treeview))
    update_button.grid(row=0, column=1, pady=30)

    delete_button = Button(button_frame, text='DELETE', font=('times new roman', 14), bg='sky blue', width=10,
                           cursor='hand2', command=lambda: delete_category(idEntry.get(), treeview))
    delete_button.grid(row=0, column=2, padx=20, pady=30)

    clear_button = Button(button_frame, text='CLEAR', font=('times new roman', 14), bg='sky blue', width=10,
                          cursor='hand2',
                          command=lambda: clear(idEntry, catEntry, descriptionText, treeview))
    clear_button.grid(row=0, column=3, pady=30)

    treeview_frame= Frame(category_frame, bg='white')
    treeview_frame.place(x=630, y=380, height=300, width=500)

    scrolly = Scrollbar(treeview_frame, orient=VERTICAL)
    scrollx = Scrollbar(treeview_frame, orient=HORIZONTAL)
    treeview = ttk.Treeview(treeview_frame, columns=('id', 'cat', 'description'), show='headings',
                            yscrollcommand=scrolly.set,
                            xscrollcommand=scrollx.set)
    scrolly.pack(side=RIGHT, fill='y')
    scrollx.pack(side=BOTTOM, fill='x')
    scrolly.config(command=treeview.yview)
    scrollx.config(command=treeview.xview)
    treeview.pack(fill=BOTH, expand=1)
    treeview.heading('id', text='ID')
    treeview.heading('cat', text='Category')
    treeview.heading('description', text='Description')

    treeview.column('id', width=80)
    treeview.column('cat', width=160)
    treeview.column('description', width=300)

    treeview_data(treeview)
    treeview.bind('<Double-1>',
                  lambda event: select_data(event, idEntry, catEntry, descriptionText, treeview))

    return category_frame
