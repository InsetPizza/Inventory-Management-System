from tkinter import *
import datetime
from tkinter import ttk
from tkcalendar import DateEntry
import pymysql
from tkinter import messagebox


def create_database_table():
    cursor, connection = connect_database()
    cursor.execute('CREATE DATABASE IF NOT EXISTS inventory_system')
    cursor.execute('USE inventory_system')
    cursor.execute('CREATE TABLE IF NOT EXISTS employee_data(empid INT PRIMARY KEY, '
                   'name VARCHAR(100), email VARCHAR(100),gender VARCHAR(50),'
                   ' dob VARCHAR(50), contact VARCHAR(50), emptype VARCHAR(50),'
                   ' education VARCHAR(30), workshift VARCHAR(50), address VARCHAR(200),'
                   ' doj VARCHAR(50), salary VARCHAR(50), usertype VARCHAR(50), password VARCHAR(50))')


# ----------------------------------------------------------------

def treeview_data():
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute('use inventory_system')
    try:
        cursor.execute('SELECT * FROM employee_data')
        employee_records = cursor.fetchall()
        emp_tv.delete(*emp_tv.get_children())
        for record in employee_records:
            emp_tv.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()


# -----------------------------------------------------------------------------------------------------------------------

def connect_database():
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='Your_password_here')
        cursor = connection.cursor()
    except:
        messagebox.showerror('Error', 'Database connection failed.')
        return None, None
    return cursor, connection


# -----------------------------------------------------------------------------------------------------------------

def select_data(event, empidEntry, nameEntry, emailEntry,
                gender_combobox, dob_date_entry, contactEntry,
                emptype_combobox, edu_combobox, ws_combobox,
                addTextArea, doj_date_entry, ut_combobox,
                salaryEntry, pwdEntry):
    index = emp_tv.selection()
    content = emp_tv.item(index)
    row = content['values']
    clear_fields(empidEntry, nameEntry, emailEntry,
                 gender_combobox, dob_date_entry, contactEntry,
                 emptype_combobox, edu_combobox, ws_combobox,
                 addTextArea, doj_date_entry, ut_combobox,
                 salaryEntry, pwdEntry, False)
    empidEntry.insert(0, row[0])
    nameEntry.insert(0, row[1])
    emailEntry.insert(0, row[2])
    gender_combobox.set(row[3])
    dob_date_entry.set_date(row[4])
    contactEntry.insert(0, row[5])
    emptype_combobox.set(row[6])
    edu_combobox.set(row[7])
    ws_combobox.set(row[8])
    addTextArea.insert(1.0, row[9])
    doj_date_entry.set_date(row[10])
    ut_combobox.set(row[12])
    salaryEntry.insert(0, row[11])
    pwdEntry.insert(0, row[13])


# -----------------------------------------------------------------------------------------------

def add_employee(empid, name, email, gender, dob_date_entry, contact, emptype, edu, ws, addTextArea, doj, ut, salary,
                 pwd):
    if (
            empid == '' or name == '' or email == '' or gender == 'Select gender' or contact == '' or emptype == 'Select Type' or edu == 'Select Education'
            or ws == 'Select Work Shift' or addTextArea == '\n' or salary == '' or ut == 'Select User Type' or pwd == ''):
        messagebox.showerror('Error', 'All fields are required.')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        cursor.execute('use inventory_system')
        try:
            cursor.execute('SELECT empid from employee_data WHERE empid=%s', (empid,))
            if cursor.fetchone():
                messagebox.showerror('Error', 'Employee ID already exists.')
                return
            address = addTextArea.strip()
            sql = """INSERT INTO employee_data (empid, name, email, gender, dob, contact,
                                                emptype, education, workshift, address, doj,
                                                salary, usertype, password)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

            values = (empid, name, email, gender, dob_date_entry, contact, emptype, edu, ws, addTextArea, doj, salary,
                      ut, pwd)

            cursor.execute(sql, values)
            connection.commit()
            treeview_data()
            messagebox.showinfo('success', 'Data added successfully.')
        except pymysql.Error as e:
            messagebox.showerror('Error', f'Error due to: {e}')
            connection.rollback()
            connection.close()


# ----------------------------------------------------------------------------------------------------------

def clear_fields(empidEntry, nameEntry, emailEntry,
                 gender_combobox, dob_date_entry, contactEntry,
                 emptype_combobox, edu_combobox, ws_combobox,
                 addTextArea, doj_date_entry, ut_combobox,
                 salaryEntry, pwdEntry, check):
    empidEntry.delete(0, END)
    nameEntry.delete(0, END)
    emailEntry.delete(0, END)
    gender_combobox.set('Select Gender')
    from datetime import date
    dob_date_entry.delete(0, END)
    contactEntry.delete(0, END)
    emptype_combobox.set('Select Type')
    edu_combobox.set('Select Education')
    ws_combobox.set('Select Work Shift')
    addTextArea.delete(1.0, END)
    doj_date_entry.set_date(date.today())
    ut_combobox.set('Select User Type')
    pwdEntry.delete(0, END)
    salaryEntry.delete(0, END)
    if check:
        emp_tv.selection_remove(emp_tv.selection())


# -----------------------------------------------------------------------------------------------

def update_emp(empid, name, email, gender, dob_date_entry, contact, emptype, edu, ws, addTextArea, doj, ut, salary,
               pwd):
    selected = emp_tv.selection()
    if not selected:
        messagebox.showerror('Error', 'No employee selected.')
        return
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('use inventory_system')
            cursor.execute('SELECT * from employee_data WHERE empid=%s', (empid,))
            current_data = cursor.fetchone()
            current_data = tuple(map(str, current_data[1:]))
            clean_address = addTextArea.strip()
            new_data = (name, email, gender, dob_date_entry, contact, emptype, edu, ws, clean_address, doj, salary, ut,
                        pwd)

            if current_data == new_data:
                messagebox.showinfo('Info', 'No changes made.')
                return

            cursor.execute('UPDATE employee_data SET name=%s, email=%s, gender=%s, '
                           'dob=%s, contact=%s, emptype=%s, education=%s, workshift=%s, '
                           'address=%s, doj=%s, salary=%s, usertype=%s, password=%s WHERE empid=%s',
                           (name, email, gender, dob_date_entry, contact, emptype, edu, ws, clean_address, doj, salary,
                            ut,
                            pwd, empid))
            connection.commit()
            treeview_data()
            messagebox.showinfo('success', 'Data updated successfully.')

        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()


# ------------------------------------------------------------------------------------------------------------------

def delete_emp(empid, ):
    selected = emp_tv.selection()
    if not selected:
        messagebox.showerror('Error', 'No employee selected.')
        return
    else:
        result = messagebox.askyesno('Confirm', 'Are you sure you want to delete this employee record?')
        if result:
            cursor, connection = connect_database()
            if not cursor or not connection:
                return
            try:
                cursor.execute('use inventory_system')
                cursor.execute('DELETE from employee_data WHERE empid=%s', (empid,))
                connection.commit()
                treeview_data()
                messagebox.showinfo('success', 'Employee record deleted successfully.')
            except Exception as e:
                messagebox.showerror('Error', f'Error due to {e}')
            finally:
                cursor.close()
                connection.close()


# -------------------------------------------------------------------------

def search_emp(search_option, value):
    allowed_columns = {
        'Employee ID': 'empid',
        'Name': 'name',
        'E-mail': 'email',
        'Gender': 'gender',
        'Employment Type': 'emptype',
        'Education': 'education',
        'Work Shift': 'workshift',
        'User Type': 'usertype',
    }
    if search_option == 'Search By':
        messagebox.showerror('Error', 'No option is selected')
    elif value == '':
        messagebox.showerror('Error', 'Enter value to search')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            columntosearch = allowed_columns[search_option]
            cursor.execute('use inventory_system')
            query = f"SELECT * from employee_data WHERE {columntosearch} LIKE %s"
            search_value = f"%{value}%"
            cursor.execute(query, (search_value,))
            records = cursor.fetchall()
            emp_tv.delete(*emp_tv.get_children())
            for record in records:
                emp_tv.insert('', END, values=record)
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()


# ------------------------------------------------------------------------------

def show_all(search_entry, search_combobox):
    treeview_data()
    search_entry.delete(0, END)
    search_combobox.set('Search By')


# -----------------------------------------------------------------------------------------------------------------------

def employee_form(root):
    global back_image, emp_tv
    employee_frame = Frame(root, bg='white')
    employee_frame.place(x=300, y=100, width=1230, height=750)
    headingLabel = Label(employee_frame, text="Manage Employee Details", font=('times new roman', 16, 'bold'),
                         bg='sky blue')
    headingLabel.place(x=0, y=0, relwidth=1)
    back_image = PhotoImage(file='back.png')
    back_button = Button(employee_frame, image=back_image, bg='white', bd=0, cursor='hand2',
                         command=lambda: employee_frame.place_forget())
    back_button.place(x=10, y=30)

    topFrame = Frame(employee_frame, bg='white')
    topFrame.place(x=0, y=60, relwidth=1, height=235)
    search_frame = Frame(topFrame, bg='white')
    search_frame.pack()
    search_combobox = ttk.Combobox(search_frame,
                                   values=('Employee ID', 'Name', "E-mail", 'Gender', 'Employment Type', 'Education',
                                           'Work Shift', 'User Type'), font=('times new roman', 12),
                                   state='readonly')
    search_combobox.set('Search By')
    search_combobox.grid(row=0, column=0)
    search_entry = Entry(search_frame, font=('times new roman', 12), bg='lightyellow')
    search_entry.grid(row=0, column=1, padx=20)
    search_button = Button(search_frame, text='SEARCH', font=('times new roman', 12), bg='sky blue', width=10,
                           cursor='hand2', command=lambda: search_emp(search_combobox.get(), search_entry.get()))
    search_button.grid(row=0, column=2, padx=20)

    show_button = Button(search_frame, text='SHOW ALL', font=('times new roman', 12), bg='sky blue', width=10,
                         cursor='hand2', command=lambda: show_all(search_entry, search_combobox))
    show_button.grid(row=0, column=3)

    hori_scroll = Scrollbar(topFrame, orient=HORIZONTAL)
    vert_scroll = Scrollbar(topFrame, orient=VERTICAL)
    emp_tv = ttk.Treeview(topFrame,
                          columns=('empid', 'name', 'email', 'gender', 'dob', 'contact', 'emptype', 'education',
                                   'workshift', 'address', 'doj', 'salary', 'usertype'), show='headings',
                          yscrollcommand=vert_scroll.set, xscrollcommand=hori_scroll.set)
    hori_scroll.pack(side=BOTTOM, fill='x')
    vert_scroll.pack(side=RIGHT, fill='y', pady=(10, 0))
    hori_scroll.config(command=emp_tv.xview)
    vert_scroll.config(command=emp_tv.yview)
    emp_tv.pack(pady=(10, 0))

    emp_tv.heading('empid', text='Employee ID')
    emp_tv.heading('name', text='Name')
    emp_tv.heading('email', text='E-mail')
    emp_tv.heading('gender', text='Gender')
    emp_tv.heading('dob', text='Date of Birth')
    emp_tv.heading('contact', text='Contact')
    emp_tv.heading('emptype', text='Employment Type')
    emp_tv.heading('education', text='Education')
    emp_tv.heading('workshift', text='Work Shift')
    emp_tv.heading('address', text='Address')
    emp_tv.heading('doj', text='Date of Joining')
    emp_tv.heading('salary', text='Salary')
    emp_tv.heading('usertype', text='User Type')

    emp_tv.column('empid', width=60)
    emp_tv.column('name', width=140)
    emp_tv.column('email', width=180)
    emp_tv.column('gender', width=80)
    emp_tv.column('dob', width=100)
    emp_tv.column('contact', width=100)
    emp_tv.column('emptype', width=120)
    emp_tv.column('education', width=120)
    emp_tv.column('workshift', width=100)
    emp_tv.column('address', width=200)
    emp_tv.column('doj', width=100)
    emp_tv.column('salary', width=140)
    emp_tv.column('usertype', width=120)

    treeview_data()

    detail_frame = Frame(employee_frame, bg='white')
    detail_frame.place(x=20, y=300, relwidth=1)
    empidLabel = Label(detail_frame, text='Employee ID', bg='white', font=('times new roman', 12))
    empidLabel.grid(row=0, column=0, padx=20, pady=10, sticky='w')
    empidEntry = Entry(detail_frame, width=20, bg='lightyellow', font=('times new roman', 12))
    empidEntry.grid(row=0, column=1, padx=20, pady=10)
    nameLabel = Label(detail_frame, text='Name', bg='white', font=('times new roman', 12))
    nameLabel.grid(row=0, column=2, padx=20, pady=10, sticky='w')
    nameEntry = Entry(detail_frame, width=20, bg='lightyellow', font=('times new roman', 12))
    nameEntry.grid(row=0, column=3, padx=20, pady=10)
    emailLabel = Label(detail_frame, text='E-mail', bg='white', font=('times new roman', 12))
    emailLabel.grid(row=0, column=4, padx=20, pady=10, sticky='w')
    emailEntry = Entry(detail_frame, width=20, bg='lightyellow', font=('times new roman', 12))
    emailEntry.grid(row=0, column=5, padx=20, pady=10)
    genderLabel = Label(detail_frame, text='Gender', bg='white', font=('times new roman', 12))
    genderLabel.grid(row=1, column=0, padx=20, pady=10, sticky='w')
    gender_combobox = ttk.Combobox(detail_frame, values=('Male', 'Female', 'Other'), font=('times new roman', 12),
                                   width=18,
                                   state='readonly')
    gender_combobox.set('Select Gender')
    gender_combobox.grid(row=1, column=1)
    dobLabel = Label(detail_frame, text='Date of Birth', bg='white', font=('times new roman', 12))
    dobLabel.grid(row=1, column=2, padx=20, pady=10, sticky='w')
    dob_date_entry = DateEntry(detail_frame, width=18, font=('times new roman', 12), date_pattern='dd/MM/yyyy')
    dob_date_entry.grid(row=1, column=3)
    contactLabel = Label(detail_frame, text='Contact', bg='white', font=('times new roman', 12))
    contactLabel.grid(row=1, column=4, padx=20, pady=10, sticky='w')
    contactEntry = Entry(detail_frame, width=20, bg='lightyellow', font=('times new roman', 12))
    contactEntry.grid(row=1, column=5, padx=20, pady=10)
    emptypeLabel = Label(detail_frame, text='Employment Type', bg='white', font=('times new roman', 12))
    emptypeLabel.grid(row=2, column=0, padx=20, pady=10, sticky='w')
    emptype_combobox = ttk.Combobox(detail_frame, values=('Full Time', 'Part Time', 'Casual', 'Contract', 'Intern'),
                                    font=('times new roman', 12), width=18,
                                    state='readonly')
    emptype_combobox.set('Select Type')
    emptype_combobox.grid(row=2, column=1)
    eduLabel = Label(detail_frame, text='Education', bg='white', font=('times new roman', 12))
    eduLabel.grid(row=2, column=2, padx=20, pady=10, sticky='w')
    edu_combobox = ttk.Combobox(detail_frame,
                                values=('B.Tech', 'B.Com', 'M.Tech', 'B.Sc', 'M.Sc', 'BBA', 'MBA', "LLB", 'LLM',
                                        'B.Arch', 'M.Arch'), font=('times new roman', 12), width=18,
                                state='readonly')
    edu_combobox.set('Select Education')
    edu_combobox.grid(row=2, column=3)
    wsLabel = Label(detail_frame, text='Work Shift', bg='white', font=('times new roman', 12))
    wsLabel.grid(row=2, column=4, padx=20, pady=10, sticky='w')
    ws_combobox = ttk.Combobox(detail_frame, values=('Morning', 'Afternoon', 'Night'), font=('times new roman', 12),
                               width=18,
                               state='readonly')
    ws_combobox.set('Select Work Shift')
    ws_combobox.grid(row=2, column=5)

    addLabel = Label(detail_frame, text='Address', bg='white', font=('times new roman', 12))
    addLabel.grid(row=3, column=0, padx=20, pady=10, sticky='w')
    addTextArea = Text(detail_frame, width=20, height=4, bg='lightyellow', font=('times new roman', 12))
    addTextArea.grid(row=3, column=1, padx=20, pady=10, rowspan=2)

    dojLabel = Label(detail_frame, text='Date of Joining', bg='white', font=('times new roman', 12))
    dojLabel.grid(row=3, column=2, padx=20, pady=10, sticky='w')
    doj_date_entry = DateEntry(detail_frame, width=18, font=('times new roman', 12), date_pattern='dd/MM/yyyy')
    doj_date_entry.grid(row=3, column=3)

    utLabel = Label(detail_frame, text='User Type', bg='white', font=('times new roman', 12))
    utLabel.grid(row=4, column=2, padx=20, pady=10, sticky='w')
    ut_combobox = ttk.Combobox(detail_frame, values=('Admin', 'Employee'), font=('times new roman', 12),
                               width=18,
                               state='readonly')
    ut_combobox.set('Select User Type')
    ut_combobox.grid(row=4, column=3)
    salaryLabel = Label(detail_frame, text='Salary', bg='white', font=('times new roman', 12))
    salaryLabel.grid(row=3, column=4, padx=20, pady=10, sticky='w')
    salaryEntry = Entry(detail_frame, width=20, bg='lightyellow', font=('times new roman', 12))
    salaryEntry.grid(row=3, column=5, padx=20, pady=10)
    pwdLabel = Label(detail_frame, text='Password', bg='white', font=('times new roman', 12))
    pwdLabel.grid(row=4, column=4, padx=20, pady=10, sticky='w')
    pwdEntry = Entry(detail_frame, width=20, bg='lightyellow', font=('times new roman', 12))
    pwdEntry.grid(row=4, column=5, padx=20, pady=10)

    button_frame = Frame(employee_frame, bg='white')
    button_frame.place(x=200, y=550)
    add_button = Button(button_frame, text='ADD', font=('times new roman', 12), bg='sky blue', width=10,
                        cursor='hand2',
                        command=lambda: add_employee(empidEntry.get(), nameEntry.get(), emailEntry.get(),
                                                     gender_combobox.get(), dob_date_entry.get(), contactEntry.get(),
                                                     emptype_combobox.get(), edu_combobox.get(), ws_combobox.get(),
                                                     addTextArea.get(1.0, END), doj_date_entry.get(), ut_combobox.get(),
                                                     salaryEntry.get(), pwdEntry.get()))
    add_button.grid(row=0, column=1, padx=20, pady=10)
    up_button = Button(button_frame, text='UPDATE', font=('times new roman', 12), bg='sky blue', width=10,
                       cursor='hand2', command=lambda: update_emp(empidEntry.get(), nameEntry.get(), emailEntry.get(),
                                                                  gender_combobox.get(), dob_date_entry.get(),
                                                                  contactEntry.get(),
                                                                  emptype_combobox.get(), edu_combobox.get(),
                                                                  ws_combobox.get(),
                                                                  addTextArea.get(1.0, END), doj_date_entry.get(),
                                                                  ut_combobox.get(),
                                                                  salaryEntry.get(), pwdEntry.get()))
    up_button.grid(row=0, column=2, padx=20, pady=10)
    del_button = Button(button_frame, text='DELETE', font=('times new roman', 12), bg='sky blue', width=10,
                        cursor='hand2', command=lambda: delete_emp(empidEntry.get()))
    del_button.grid(row=0, column=3, padx=20, pady=10)
    clr_button = Button(button_frame, text='CLEAR', font=('times new roman', 12), bg='sky blue', width=10,
                        cursor='hand2', command=lambda: clear_fields(empidEntry, nameEntry, emailEntry,
                                                                     gender_combobox, dob_date_entry, contactEntry,
                                                                     emptype_combobox, edu_combobox, ws_combobox,
                                                                     addTextArea, doj_date_entry, ut_combobox,
                                                                     salaryEntry, pwdEntry, True))
    clr_button.grid(row=0, column=4, padx=20, pady=10)
    emp_tv.bind('<Double-1>', lambda event: select_data(event, empidEntry, nameEntry, emailEntry,
                                                        gender_combobox, dob_date_entry, contactEntry,
                                                        emptype_combobox, edu_combobox, ws_combobox,
                                                        addTextArea, doj_date_entry, ut_combobox,
                                                        salaryEntry, pwdEntry))
    create_database_table()
    return employee_frame