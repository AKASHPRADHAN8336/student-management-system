from datetime import datetime
from tkinter import *
from tkinter import ttk, messagebox, filedialog

import pandas

entry_objects = []


# Function to display a popup window to get details from the user
def get_details(title, button_text, command, rf):
    if button_text == "Update":
        indexing = rf.student_table.focus()
        if indexing == "":
            messagebox.showwarning(title="Error", message="Select a record!")
            return

    # Create a popup window to take entries
    global entry_objects
    window = Toplevel()
    window.geometry("+50+80")
    window.resizable(False, False)
    window.grab_set()
    window.title(title)

    # Create labels and entry fields for various details
    id_label = ttk.Label(window, text="Id", font=("times new roman", 16, "bold"))
    id_label.grid(row=0, column=0, padx=20, pady=10, sticky=W)

    id_entry = ttk.Entry(
        window, font=("times new roman", 16, "bold"), width=30, show=""
    )
    id_entry.grid(row=0, column=1, padx=20, pady=10, sticky=W)
    id_entry.focus_set()

    name_label = ttk.Label(window, text="Name", font=("times new roman", 16, "bold"))
    name_label.grid(row=1, column=0, padx=20, pady=10, sticky=W)

    name_entry = ttk.Entry(
        window, font=("times new roman", 16, "bold"), width=30, show=""
    )
    name_entry.grid(row=1, column=1, padx=20, pady=10, sticky=W)
    id_entry.bind("<Return>", lambda e: name_entry.focus_set())

    gender_label = ttk.Label(
        window, text="Gender", font=("times new roman", 16, "bold")
    )
    gender_label.grid(row=2, column=0, padx=20, pady=10, sticky=W)

    gender_entry = ttk.Entry(
        window, font=("times new roman", 16, "bold"), width=30, show=""
    )
    gender_entry.grid(row=2, column=1, padx=20, pady=10, sticky=W)
    name_entry.bind("<Return>", lambda e: gender_entry.focus_set())

    phone_label = ttk.Label(window, text="Phone", font=("times new roman", 16, "bold"))
    phone_label.grid(row=3, column=0, padx=20, pady=10, sticky=W)

    phone_entry = ttk.Entry(
        window, font=("times new roman", 16, "bold"), width=30, show=""
    )
    phone_entry.grid(row=3, column=1, padx=20, pady=10, sticky=W)
    gender_entry.bind("<Return>", lambda e: phone_entry.focus_set())

    email_label = ttk.Label(window, text="Email", font=("times new roman", 16, "bold"))
    email_label.grid(row=4, column=0, padx=20, pady=10, sticky=W)

    email_entry = ttk.Entry(
        window, font=("times new roman", 16, "bold"), width=30, show=""
    )
    email_entry.grid(row=4, column=1, padx=20, pady=10, sticky=W)
    phone_entry.bind("<Return>", lambda e: email_entry.focus_set())

    dob_label = ttk.Label(window, text="DOB", font=("times new roman", 16, "bold"))
    dob_label.grid(row=5, column=0, padx=20, pady=10, sticky=W)

    dob_entry = ttk.Entry(
        window, font=("times new roman", 16, "bold"), width=30, show=""
    )
    dob_entry.grid(row=5, column=1, padx=20, pady=10, sticky=W)
    email_entry.bind("<Return>", lambda e: dob_entry.focus_set())

    marks_label = ttk.Label(window, text="marks", font=("times new roman", 16, "bold"))
    marks_label.grid(row=6, column=0, padx=20, pady=10, sticky=W)

    marks_entry = ttk.Entry(
        window, font=("times new roman", 16, "bold"), width=30, show=""
    )
    marks_entry.grid(row=6, column=1, padx=20, pady=10, sticky=W)
    dob_entry.bind("<Return>", lambda e: marks_entry.focus_set())

    entry_objects = [
        id_entry,
        name_entry,
        gender_entry,
        phone_entry,
        email_entry,
        dob_entry,
        marks_entry,
        window,
    ]

    if button_text == "Update":
        # Insert existing data into the entry fields for updating
        content = rf.student_table.item(indexing)

        list_data = content["values"]
        for i in range(len(entry_objects) - 2):
            if i == 3:
                entry_objects[3].insert(0, "+" + str(list_data[3]))
            else:
                entry_objects[i].insert(0, list_data[i])
        entry_objects[-2].insert(
            0, datetime.strptime(list_data[-2], "%Y-%m-%d").strftime("%d-%m-%Y")
        )
        entry_objects[0].config(state=DISABLED)

    button = ttk.Button(window, text=button_text, command=command)
    button.grid(row=7, columnspan=2, pady=10)


class LeftFrame:
    # Class representing the left frame of the main window

    def __init__(self, root, rt_frame):
        self.root = root
        self.rf = rt_frame
        self.left_frame = ttk.Frame(root)
        self.left_frame.place(x=50, y=80, width=140, height=600)

        self.logo_image = PhotoImage(file=r"media\admin.png")
        self.logo_label = ttk.Label(self.left_frame, image=self.logo_image)
        self.logo_label.grid(row=0, column=0, columnspan=2)

        # Create buttons for various operations
        self.add_student_button = ttk.Button(
            self.left_frame,
            text="Add Student",
            width=14,
            state=NORMAL,
            command=lambda: get_details("Add Student", "Add", self.add_student, None),
        )
        self.add_student_button.grid(row=1, column=0, pady=20)

        self.search_student_button = ttk.Button(
            self.left_frame,
            text="Search Student",
            width=14,
            state=NORMAL,
            command=lambda: get_details(
                "Search Student(s)", "Search", self.search_student, None
            ),
        )
        self.search_student_button.grid(row=2, column=0, pady=20)

        self.update_student_button = ttk.Button(
            self.left_frame,
            text="Update Student",
            width=14,
            state=NORMAL,
            command=lambda: get_details(
                "Update Student", "Update", self.update_student, self.rf
            ),
        )
        self.update_student_button.grid(row=3, column=0, pady=20)

        self.delete_student_button = ttk.Button(
            self.left_frame,
            text="Delete Student",
            width=14,
            state=NORMAL,
            command=self.rf.delete_student,
        )
        self.delete_student_button.grid(row=4, column=0, pady=20)

        self.show_student_button = ttk.Button(
            self.left_frame,
            text="Show Student",
            width=14,
            state=NORMAL,
            command=self.show_student_view,
        )
        self.show_student_button.grid(row=5, column=0, pady=20)

        self.export_button = ttk.Button(
            self.left_frame,
            text="Export Data",
            width=14,
            state=NORMAL,
            command=self.export_data,
        )
        self.export_button.grid(row=6, column=0, pady=20)

        # Add this button after the export_button in the __init__ method
        self.marks_button = ttk.Button(
            self.left_frame,
            text="Student Marks",
            width=14,
            state=NO,
            command=self.show_marks_view,
        )
        self.marks_button.grid(row=7, column=0, pady=20)

        self.current_view = "students"

    def add_student(self):
        # Get all entry values except the last one (which is the window)
        entries = [entry.get() for entry in entry_objects[:-1]]

        # Debug print to see what's being captured
        print("Raw entries:", entries)  # Add this for debugging

        if "" in entries:
            messagebox.showerror(title="Error", message="All fields are required!")
            entry_objects[0].focus_set()
            return

        try:
            # The DOB should be at index 5 (since marks is at 6)
            dob_str = entries[5]
            print("DOB string:", dob_str)  # Debug print
            dob = datetime.strptime(dob_str, "%d-%m-%Y").strftime("%Y-%m-%d")
            entries[5] = dob
        except ValueError as e:
            messagebox.showerror(
                "Date Error",
                f"Invalid date format! Please use DD-MM-YYYY\nError: {str(e)}",
            )
            entry_objects[5].focus_set()  # Focus on DOB entry
            return

        try:
            # Validate marks is a number (index 6)
            float(entries[6])
        except ValueError:
            messagebox.showerror("Marks Error", "Marks must be a number")
            entry_objects[6].focus_set()
            return

        if self.rf.add_data("student", entries):
            messagebox.showinfo("Success", "Student added successfully!")
        else:
            messagebox.showerror("Error", "Failed to add student")

        # Clear fields
        for entry in entry_objects[:-1]:
            entry.delete(0, END)
        self.rf.get_data()

    def search_student(self):
        try:
            entries = [obj.get() for obj in entry_objects[:-1]]

            # Build dynamic WHERE conditions
            conditions = []
            params = []

            # Map entry fields to database columns
            field_map = [
                ("id", entries[0]),  # id_entry -> id
                ("name", entries[1]),  # name_entry -> name
                ("gender", entries[2]),  # gender_entry -> gender
                ("phone", entries[3]),  # phone_entry -> phone
                ("email", entries[4]),  # email_entry -> email
                ("dob", entries[5]),  # dob_entry -> dob
            ]

            for field, value in field_map:
                if value:  # Only add to query if value is not empty
                    if field == "dob":
                        try:
                            # Try to parse date in DD-MM-YYYY format
                            parsed_date = datetime.strptime(value, "%d-%m-%Y").strftime(
                                "%Y-%m-%d"
                            )
                            conditions.append(f"{field} = %s")
                            params.append(parsed_date)
                        except ValueError:
                            try:
                                # Try to parse date in YYYY-MM-DD format
                                parsed_date = datetime.strptime(
                                    value, "%Y-%m-%d"
                                ).strftime("%Y-%m-%d")
                                conditions.append(f"{field} = %s")
                                params.append(parsed_date)
                            except ValueError:
                                messagebox.showerror(
                                    "Date Error",
                                    "Invalid date format! Use DD-MM-YYYY or YYYY-MM-DD",
                                )
                                return
                    else:
                        conditions.append(f"{field} LIKE %s")
                        params.append(f"%{value}%")

            if not conditions:
                messagebox.showwarning(
                    "Search Error", "Please enter at least one search criteria"
                )
                return

            query = "SELECT * FROM student WHERE " + " AND ".join(conditions)
            self.rf.my_cursor.execute(query, tuple(params))
            self.rf.show_data()

        except Exception as e:
            messagebox.showerror("Search Error", f"Failed to search: {str(e)}")

    def update_student(self):
        # Function to update a student based on the entered details

        window = entry_objects[-1]
        entries = [entry.get() for entry in entry_objects[:-1]]
        entries[1] = entries[1].title()
        entries[2] = entries[2].title()
        entries[-1] = datetime.strptime(entries[-1], "%d-%m-%Y").strftime("%Y-%m-%d")
        query_entries = tuple(entries[1:] + [entries[0]])
        if self.rf.update_and_show(query_entries):
            messagebox.showinfo(
                "Success", f"Id {entries[0]} is modified successfully", parent=window
            )
            window.destroy()

    def export_data(self):
        # Function to export the student data to a CSV file

        url = filedialog.asksaveasfilename(defaultextension=".csv")
        indexing = self.rf.student_table.get_children()
        new_list = []
        for index in indexing:
            content = self.rf.student_table.item(index)
            data_list = content["values"]
            new_list.append(data_list)

        table = pandas.DataFrame(
            new_list,
            columns=[
                "Id",
                "Name",
                "Mobile",
                "Email",
                "Gender",
                "DOB",
                "Added Date",
                "marks",
            ],
        )
        table.to_csv(url, index=False)
        messagebox.showinfo("Success", "Data is saved successfully")

    def show_marks_view(self):
        """Switch to marks view"""
        self.rf.setup_marks_view()
        self.rf.show_marks()
        self.current_view = "marks"

    def show_student_view(self):
        """Switch to student details view"""
        self.rf.setup_student_view()  # Reset to student view first
        self.rf.get_data()  # Then get fresh student data
        self.current_view = "students"
