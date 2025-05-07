from tkinter import *
from tkinter import ttk, messagebox
import pymysql
from tkinter import messagebox


class RightFrame:
    def __init__(self, root):
        self.root = root
        self.connect_data_base()
        self.root = root
        self.column_sort_order = {}
        right_frame = ttk.Frame(root)
        right_frame.place(x=300, y=80, width=1040, height=600)

        # Create the scrollbar widget
        scroll_bar_x = ttk.Scrollbar(right_frame, orient=HORIZONTAL)
        scroll_bar_y = ttk.Scrollbar(right_frame, orient=VERTICAL)

        # Create the Treeview widget to display data
        self.student_table = ttk.Treeview(right_frame, 
                                        columns=('Id', 'Name', 'Gender', 'Mobile', 'Email', 'DOB', 'Added Date','marks'),
                                        xscrollcommand=scroll_bar_x.set, 
                                        yscrollcommand=scroll_bar_y.set,
                                        show='headings')
        self.student_table.pack(fill=BOTH, expand=1)

        scroll_bar_x.config(command=self.student_table.xview)
        scroll_bar_y.config(command=self.student_table.yview)

        scroll_bar_x.pack(side=BOTTOM, fill=X)
        scroll_bar_y.pack(side=RIGHT, fill=Y)

        # Store original column configuration
        self.original_columns = ('Id', 'Name', 'Gender', 'Mobile', 'Email', 'DOB', 'Added Date','marks')
        self.current_view = 'students'  # Track current view
        
        # Initialize with student view
        self.setup_student_view()
        self.get_data()

    def setup_student_view(self):
        """Configure the table for student data view"""
        self.current_view = 'students'
        self.student_table['columns'] = self.original_columns
        
        # Clear existing columns
        for col in self.student_table['columns']:
            self.student_table.heading(col, text='')
        
        # Set column headings with sorting
        self.student_table.heading('Id', text='Id', command=lambda: self.sort_by_column('Id'))
        self.student_table.heading('Name', text='Name', command=lambda: self.sort_by_column('Name'))
        self.student_table.heading('Gender', text='Gender', command=lambda: self.sort_by_column('Gender'))
        self.student_table.heading('Mobile', text='Mobile', command=lambda: self.sort_by_column('Mobile'))
        self.student_table.heading('Email', text='Email', command=lambda: self.sort_by_column('Email'))
        self.student_table.heading('DOB', text='DOB', command=lambda: self.sort_by_column('DOB'))
        self.student_table.heading('Added Date', text='Added Date', command=lambda: self.sort_by_column('Added_Date'))
        self.student_table.heading('marks', text='marks', command=lambda: self.sort_by_column('marks'))
        
        # Set column widths
        self.student_table.column('Id', width=50)
        self.student_table.column('Name', width=150)
        self.student_table.column('Gender', width=80)
        self.student_table.column('Mobile', width=120)
        self.student_table.column('Email', width=200)
        self.student_table.column('DOB', width=100)
        self.student_table.column('Added Date', width=120)
        self.student_table.column('marks', width=120)

    def setup_marks_view(self):
        """Configure the table for marks data view"""
        self.current_view = 'marks'
        self.student_table['columns'] = ('Id', 'Name', 'ADBMS', 'PYTHON', 'HCI')
        
        # Clear existing columns
        for col in self.student_table['columns']:
            self.student_table.heading(col, text='')
        
        # Set column headings (no sorting for marks)
        self.student_table.heading('Id', text='ID')
        self.student_table.heading('Name', text='Name')
        self.student_table.heading('ADBMS', text='ADBMS')
        self.student_table.heading('PYTHON', text='PYTHON')
        self.student_table.heading('HCI', text='HCI')
        
        # Set column widths
        self.student_table.column('Id', width=50)
        self.student_table.column('Name', width=150)
        self.student_table.column('ADBMS', width=80)
        self.student_table.column('PYTHON', width=80)
        self.student_table.column('HCI', width=80)

    def connect_data_base(self):
        entries = {'host': '127.0.0.1', 'user': 'root', 'password': '#Bollywood20'}
        try:
            connection = pymysql.connect(host=entries['host'], user=entries['user'],
                                      password=entries['password'])
            cursor = connection.cursor()
        except Exception as e:
            messagebox.showerror(title='Error', message='Cannot Connect to data base')
            exit()
        else:
            self.my_cursor = cursor
            self.my_connection = connection
            cursor.execute('use student_management')
            messagebox.showinfo(title='Success!',
                              message='Database connection is successful!')
        return True

    def show_data(self):
        self.student_table.delete(*self.student_table.get_children())
        fetched_data = self.my_cursor.fetchall()
        for data in fetched_data:
            data_list = list(data)
            self.student_table.insert('', END, values=data_list)

   
    
    def add_data(self, table, entries):
        # Explicitly list the columns you're inserting into (excluding added_date since it has a default)
        query = f'INSERT INTO {table} (id, name, gender, phone, email, dob,added_date,marks) VALUES (%s, %s, %s, %s, %s, %s,CURDATE(),%s)'
        try:
            self.my_cursor.execute(query, entries)
            self.my_connection.commit()
            self.get_data()
        except Exception as e:
            messagebox.showerror(title='Error', message=f'{e}')
            return False
        return True

    def get_data(self, table='student', order_by='added_date', order='ASC', condition='id!=0'):
        if self.current_view == 'students':
            query = f"SELECT * FROM {table} WHERE {condition} ORDER BY {order_by} {order}"
        else:
            query = """
            SELECT s.id, s.name, 
                   COALESCE(m.ADBMS, 0) as ADBMS, 
                   COALESCE(m.PYTHON, 0) as PYTHON, 
                   COALESCE(m.HCI, 0) as HCI 
            FROM student s 
            LEFT JOIN marks m ON s.id = m.id
            WHERE s.id != 0
            ORDER BY s.id
            """
        
        self.my_cursor.execute(query)
        self.show_data()

    def sort_by_column(self, column):
        if self.current_view != 'students':
            return  # Disable sorting for marks view
            
        if column in self.column_sort_order:
            if self.column_sort_order[column] == 'ASC':
                self.get_data(order_by=column, order='ASC')
                self.column_sort_order[column] = 'DESC'
            else:
                self.get_data(order_by=column, order='DESC')
                self.column_sort_order[column] = 'ASC'
        else:
            self.get_data(order_by=column, order='ASC')
            self.column_sort_order[column] = 'DESC'

    def search_data(self, query, params):
        self.my_cursor.execute(query, params)
        self.show_data()

    def delete_student(self):
        indexing = self.student_table.focus()
        content = self.student_table.item(indexing)
        content_id = content['values'][0]
        query = 'DELETE FROM student WHERE id=%s'
        self.my_cursor.execute(query, content_id)
        self.my_connection.commit()
        self.get_data()
        messagebox.showinfo('Deleted', f'Id {content_id} is deleted successfully')

    def update_and_show(self, entries):
        query = 'update student set name=%s,gender=%s, phone=%s,email=%s,dob=%s, added_date=CURDATE(),marks=%s where id=%s'
        try:
            self.my_cursor.execute(query, entries)
        except Exception as e:
            messagebox.showerror(title='Error', message=f'{e}')
            return False
        else:
            self.my_connection.commit()
            self.get_data()
            return True
        
    def show_marks(self):
        """Display student marks view"""
        self.setup_marks_view()
        try:
            query = """
            SELECT s.id, s.name, 
                   COALESCE(m.ADBMS, 0) as ADBMS, 
                   COALESCE(m.PYTHON, 0) as PYTHON, 
                   COALESCE(m.HCI, 0) as HCI 
            FROM student s 
            LEFT JOIN marks m ON s.id = m.id
            WHERE s.id != 0
            ORDER BY s.id
            """
            self.my_cursor.execute(query)
            self.show_data()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch marks: {str(e)}")
            # Revert to student view on error
            self.setup_student_view()
            self.get_data()
