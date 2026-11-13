# ===============================================
#       NMT12704 PROGRAMMING TECHNOLOGY II
#           ASSIGNMENT MANAGEMENT
# 
# ===============================================
# 
# NIK MOHAMAD AZIZI BIN NIK YAHYA (241503239)
# AFIFAH NADHIRAH BINTI SELBINI (241501822)
# NISA LIYANA BINTI ASMADI (241501842)
# 
# ===============================================

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
import csv
from datetime import datetime, timedelta
import json
import os
from calendar import monthrange


class AssignmentManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Assignment Manager")
        self.root.geometry("1100x700")
        self.root.minsize(1000, 600)
        
        # Initialize data storage
        self.courses = []
        self.assignments = []
        self.load_data()
        
        # Color scheme
        self.bg_color = "#ffffff"  # Pure white
        self.sidebar_color = "#f0f8ff"  # Very light blue
        self.primary_color = "#0066cc"  # Medium blue
        self.danger_color = "#cc0000"  # Red for delete buttons
        self.text_color = "#000000"  # Black
        self.card_border = "#0066cc"  # Blue border for cards
        self.success_color = "#008000"  # Green for success
        
        # Configure styles
        self.configure_styles()
        
        # Create UI
        self.create_sidebar()
        self.create_main_content()
        
        # Show default view
        self.show_dashboard()
    
    def load_data(self):
        """Load data from JSON files if they exist"""
        try:
            if os.path.exists('courses.json'):
                with open('courses.json', 'r') as f:
                    self.courses = json.load(f)
            
            if os.path.exists('assignments.json'):
                with open('assignments.json', 'r') as f:
                    self.assignments = json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
    
    def save_data(self):
        """Save data to JSON files"""
        try:
            with open('courses.json', 'w') as f:
                json.dump(self.courses, f)
            
            with open('assignments.json', 'w') as f:
                json.dump(self.assignments, f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")
    
    def configure_styles(self):
        """Configure clean widget styles"""
        style = ttk.Style()
        
        # Base frame style
        style.configure('TFrame', background=self.bg_color)
        
        # Sidebar styles
        style.configure('Sidebar.TFrame', background=self.sidebar_color)
        style.configure('Sidebar.TLabel', 
                      background=self.sidebar_color,
                      foreground=self.text_color,
                      font=('Arial', 11))
        
        style.configure('Sidebar.TButton',
                      background=self.sidebar_color,
                      foreground=self.text_color,
                      font=('Arial', 10),
                      borderwidth=0,
                      anchor='w',
                      padding=(15, 8))
        
        style.map('Sidebar.TButton',
                background=[('active', '#e6f2ff')],
                foreground=[('active', self.primary_color)])
        
        # Main content styles
        style.configure('Header.TLabel',
                      background=self.bg_color,
                      foreground=self.text_color,
                      font=('Arial', 14, 'bold'))
        
        # Card style with blue border
        style.configure('Card.TFrame',
                      background=self.bg_color,
                      relief='solid',
                      borderwidth=1,
                      bordercolor=self.card_border)
        
        # LabelFrame style
        style.configure('TLabelframe', 
                       background=self.bg_color,
                       bordercolor=self.primary_color)
        
        style.configure('TLabelframe.Label',
                      background=self.bg_color,
                      foreground=self.primary_color,
                      font=('Arial', 10, 'bold'))
        
        # Button styles
        style.configure('Primary.TButton',
                      background=self.bg_color,
                      foreground=self.primary_color,
                      font=('Arial', 10, 'bold'),
                      borderwidth=1,
                      bordercolor=self.primary_color,
                      padding=8)
        
        style.map('Primary.TButton',
                background=[('active', '#e6f2ff')])
        
        style.configure('Secondary.TButton',
                      background=self.bg_color,
                      foreground=self.text_color,
                      font=('Arial', 10),
                      borderwidth=1,
                      bordercolor="#cccccc",
                      padding=8)
        
        style.map('Secondary.TButton',
                background=[('active', '#f5f5f5')])
        
        style.configure('Danger.TButton',
                      background=self.bg_color,
                      foreground=self.danger_color,
                      font=('Arial', 10),
                      borderwidth=1,
                      bordercolor=self.danger_color,
                      padding=8)
        
        style.map('Danger.TButton',
                background=[('active', '#ffebee')])
        
        style.configure('Success.TButton',
                      background=self.bg_color,
                      foreground=self.success_color,
                      font=('Arial', 10),
                      borderwidth=1,
                      bordercolor=self.success_color,
                      padding=8)
        
        style.map('Success.TButton',
                background=[('active', '#e6ffe6')])
        
        # Entry styles
        style.configure('TEntry',
                      fieldbackground='white',
                      foreground=self.text_color,
                      bordercolor=self.primary_color,
                      padding=(10, 5))
        
        # Combobox styles
        style.configure('TCombobox',
                      fieldbackground='white',
                      foreground=self.text_color,
                      selectbackground=self.primary_color,
                      selectforeground='white',
                      padding=(8, 5),
                      bordercolor=self.primary_color)
        
        # Treeview styles
        style.configure('Treeview',
                      font=('Arial', 10),
                      rowheight=30,
                      background='white',
                      fieldbackground='white',
                      foreground=self.text_color,
                      bordercolor=self.primary_color)
        
        style.configure('Treeview.Heading',
                      font=('Arial', 10, 'bold'),
                      background=self.sidebar_color,
                      foreground=self.text_color,
                      relief='flat',
                      padding=(10, 5))
        
        style.map('Treeview',
                background=[('selected', self.primary_color)],
                foreground=[('selected', 'white')])
    
    def create_sidebar(self):
        """Create clean sidebar navigation"""
        self.sidebar = ttk.Frame(self.root, style='Sidebar.TFrame', width=220)
        self.sidebar.pack(side='left', fill='y')
        self.sidebar.pack_propagate(False)
        
        # Title
        title_frame = ttk.Frame(self.sidebar, style='Sidebar.TFrame')
        title_frame.pack(pady=(25, 30), padx=15, fill='x')
        
        ttk.Label(title_frame, 
                text="Assignment Manager", 
                style='Sidebar.TLabel',
                font=('Arial', 12, 'bold')).pack(anchor='w')
        
        # Navigation menu
        nav_frame = ttk.Frame(self.sidebar, style='Sidebar.TFrame')
        nav_frame.pack(fill='x', padx=10)
        
        nav_items = [
            ("Dashboard View", self.show_dashboard),
            ("Subjects View", self.show_courses),
            ("Assignments View", self.show_assignments),
            ("Export CSV", self.export_assignments),
            ("Exit", self.root.quit)
        ]
        
        for text, command in nav_items:
            btn = ttk.Button(nav_frame, 
                            text=text, 
                            style='Sidebar.TButton', 
                            command=command)
            btn.pack(fill='x', pady=2)
    
    def create_main_content(self):
        """Create the main content area"""
        self.main_content = ttk.Frame(self.root)
        self.main_content.pack(side='right', fill='both', expand=True)
        
        # Header
        self.header = ttk.Frame(self.main_content, height=70)
        self.header.pack(fill='x')
        self.header.pack_propagate(False)
        
        self.header_content = ttk.Frame(self.header)
        self.header_content.pack(fill='both', expand=True, padx=25)
        
        self.header_label = ttk.Label(self.header_content, 
                                    text="Dashboard", 
                                    style='Header.TLabel')
        self.header_label.pack(side='left')
        
        # Content container
        self.content = ttk.Frame(self.main_content)
        self.content.pack(fill='both', expand=True, padx=25, pady=(0, 25))
    
    def show_dashboard(self):
        """Show dashboard view"""
        self.clear_content()
        self.header_label.config(text="Dashboard")
        
        # Calculate statistics
        total_courses = len(self.courses)

        active_assignments = len([a for a in self.assignments if a['status'] != 'Completed'])
        
        overdue_assignments = len([
            a for a in self.assignments 
            if a['status'] != 'Completed' and 
            datetime.strptime(a['due_date'], "%d-%m-%Y").date() <= datetime.now().date()
        ])

        # Count assignments due this week
        today = datetime.now().date()
        week_later = today + timedelta(days=7)
        due_this_week = len([
            a for a in self.assignments 
            if a['status'] != 'Completed' and 
            today < datetime.strptime(a['due_date'], "%d-%m-%Y").date() <= week_later
        ])
        
        completed_assignments = len([a for a in self.assignments if a['status'] == 'Completed'])
        
        # Summary cards
        summary_frame = ttk.Frame(self.content)
        summary_frame.pack(fill='x', pady=(0, 25))
        
        stats = [
            ("Total Subjects", total_courses),
            ("Active Assignments", active_assignments),
            ("Due This Week", due_this_week),
            ("Overdue Assignments", overdue_assignments),
            ("Completed", completed_assignments)
        ]
        
        for i, (title, value) in enumerate(stats):
            card = ttk.Frame(summary_frame, style='Card.TFrame')
            card.grid(row=0, column=i, padx=8, pady=5, sticky='nsew')
            
            ttk.Label(card, 
                     text=title, 
                     background=self.bg_color,
                     foreground=self.text_color,
                     font=('Arial', 9)).pack(pady=(15, 0))
            
            value_color = self.primary_color
            if title == "Overdue Assignments" and value > 0:
                value_color = self.danger_color  # Red

            ttk.Label(card, 
                    text=str(value), 
                    background=self.bg_color,
                    foreground=value_color,
                    font=('Arial', 18, 'bold')).pack(pady=(0, 15))

            
            summary_frame.columnconfigure(i, weight=1)
        
        # Recent assignments
        recent_frame = ttk.LabelFrame(self.content, 
                                    text="Recent Assignments",
                                    padding=(15, 10, 15, 15))
        recent_frame.pack(fill='both', expand=True)
        
        # Treeview
        columns = ("No", "Subject", "Assignment", "Due Date", "Status")
        self.tree = ttk.Treeview(recent_frame, 
                                columns=columns, 
                                show="headings", 
                                height=8)
        
        # Configure columns
        col_widths = [60, 150, 250, 120, 100]
        for col, width in zip(columns, col_widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor='center')
        
        self.tree.column("Subject", anchor='w')
        self.tree.column("Assignment", anchor='w')
        
        # Add scrollbar
        v_scroll = ttk.Scrollbar(recent_frame, 
                                orient="vertical", 
                                command=self.tree.yview)
        self.tree.configure(yscrollcommand=v_scroll.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        
        # Configure frame grid
        recent_frame.columnconfigure(0, weight=1)
        recent_frame.rowconfigure(0, weight=1)
        
        # Add data sorted by due date (ascending)
        sorted_assignments = sorted(
            self.assignments,
            key=lambda x: datetime.strptime(x['due_date'], "%d-%m-%Y")
        )
        
        for i, assignment in enumerate(sorted_assignments[:10], start=1):  # Numbered 1–10
            course_name = assignment['course']
            course_code = next(
                (course['code'] for course in self.courses 
                if course['name'] == course_name),
                course_name  # fallback if not found
            )
            display_text = f"[{course_code}] {course_name}"

            self.tree.insert("", "end", values=(
                i,  # Use number instead of assignment['id']
                display_text,
                assignment['title'],
                assignment['due_date'],
                assignment['status']
            ))
        
        # Bind double click to show assignment details
        self.tree.bind("<Double-1>", self.show_assignment_details)
        
        # Auto-save when switching views
        self.save_data()
    
    def show_courses(self):
        """Show courses management view"""
        self.clear_content()
        self.header_label.config(text="Subject Management")
        
        # Form frame
        form_frame = ttk.LabelFrame(self.content, 
                                  text="Subject Form",
                                  padding=(20, 15, 20, 20))
        form_frame.pack(fill='x', pady=(0, 25))
        
        # Form fields - using uniform width for all inputs
        field_width = 30
        
        ttk.Label(form_frame, 
                 text="Subject Code:", 
                 background=self.bg_color,
                 foreground=self.text_color,
                 font=('Arial', 10)).grid(row=0, column=0, padx=10, pady=8, sticky='e')
        
        self.course_code = ttk.Entry(form_frame, 
                                   font=('Arial', 10),
                                   width=field_width)
        self.course_code.grid(row=0, column=1, padx=10, pady=8, sticky='w')
        
        ttk.Label(form_frame, 
                 text="Subject Name:", 
                 background=self.bg_color,
                 foreground=self.text_color,
                 font=('Arial', 10)).grid(row=1, column=0, padx=10, pady=8, sticky='e')
        
        self.course_name = ttk.Entry(form_frame, 
                                   font=('Arial', 10),
                                   width=field_width)
        self.course_name.grid(row=1, column=1, padx=10, pady=8, sticky='w')
        
        # Action buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(btn_frame, 
                  text="Add Subject", 
                  style='Primary.TButton',
                  command=self.add_course).pack(side='left', padx=5)
        
        ttk.Button(btn_frame, 
                  text="Update",
                  style='Success.TButton',
                  command=self.update_course).pack(side='left', padx=5)
        
        ttk.Button(btn_frame, 
                  text="Delete",
                  style='Danger.TButton',
                  command=self.delete_course).pack(side='left', padx=5)
        
        ttk.Button(btn_frame, 
                  text="Clear",
                  style='Secondary.TButton',
                  command=self.clear_course_form).pack(side='left', padx=5)
        
        # Courses list
        list_frame = ttk.LabelFrame(self.content, 
                                  text="Subject Catalog",
                                  padding=(15, 10, 15, 15))
        list_frame.pack(fill='both', expand=True)
        
        # Treeview
        columns = ("Subject Code", "Subject Name")
        self.course_tree = ttk.Treeview(list_frame, 
                                      columns=columns, 
                                      show="headings")
        
        # Configure columns
        col_widths = [100, 400]
        for col, width in zip(columns, col_widths):
            self.course_tree.heading(col, text=col)
            self.course_tree.column(col, width=width, anchor='center')
        
        self.course_tree.column("Subject Name", anchor='w')
        
        # Add scrollbar
        v_scroll = ttk.Scrollbar(list_frame, 
                                orient="vertical", 
                                command=self.course_tree.yview)
        self.course_tree.configure(yscrollcommand=v_scroll.set)
        
        # Grid layout
        self.course_tree.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        
        # Configure frame grid
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Add data
        for course in self.courses:
            self.course_tree.insert("", "end", values=(course['code'], course['name']))
        
        # Bind selection to populate form
        self.course_tree.bind("<<TreeviewSelect>>", self.populate_course_form)
        
        # Auto-save when switching views
        self.save_data()
    
    def show_assignments(self):
        """Show assignments management view"""
        self.clear_content()
        self.header_label.config(text="Assignment Management")
        
        # Form frame
        form_frame = ttk.LabelFrame(self.content, 
                                  text="Assignment Form",
                                  padding=(20, 15, 20, 20))
        form_frame.pack(fill='x', pady=(0, 25))
        
        # Form fields - using uniform width for all inputs
        field_width = 28  # Slightly smaller to account for combobox padding
        
        # Course selection
        ttk.Label(form_frame, 
                 text="Subject:", 
                 background=self.bg_color,
                 foreground=self.text_color,
                 font=('Arial', 10)).grid(row=0, column=0, padx=10, pady=8, sticky='e')
        
        course_name = [course['name'] for course in self.courses]
        self.assignment_course = ttk.Combobox(form_frame, 
                                            values=course_name,
                                            font=('Arial', 10),
                                            width=field_width)
        self.assignment_course.grid(row=0, column=1, padx=10, pady=8, sticky='w')
        
        # Assignment title
        ttk.Label(form_frame, 
                 text="Title:", 
                 background=self.bg_color,
                 foreground=self.text_color,
                 font=('Arial', 10)).grid(row=1, column=0, padx=10, pady=8, sticky='e')
        
        self.assignment_title = ttk.Entry(form_frame, 
                                        font=('Arial', 10),
                                        width=30)
        self.assignment_title.grid(row=1, column=1, padx=10, pady=8, sticky='w')
        
        # Due date selection (year, month, day)
        ttk.Label(form_frame, 
                 text="Due Date:", 
                 background=self.bg_color,
                 foreground=self.text_color,
                 font=('Arial', 10)).grid(row=2, column=0, padx=10, pady=8, sticky='e')
        
        # Frame to hold the date dropdowns
        date_frame = ttk.Frame(form_frame)
        date_frame.grid(row=2, column=1, padx=10, pady=8, sticky='w')
        
        
        # Day dropdown - will be updated based on month/year selection
        self.due_day = ttk.Combobox(date_frame, 
                                   font=('Arial', 10),
                                   width=4)
        self.due_day.pack(side='left', padx=2)
        
        # Month dropdown
        self.due_month = ttk.Combobox(date_frame, 
                                    values=[f"{m:02d}" for m in range(1, 13)],
                                    font=('Arial', 10),
                                    width=5)
        self.due_month.pack(side='left', padx=2)
        self.due_month.set(f"{datetime.now().month:02d}")
        
        # Year dropdown (current year and next 5 years)
        current_year = datetime.now().year
        self.due_year = ttk.Combobox(date_frame, 
                                   values=[str(y) for y in range(current_year, current_year + 2)],
                                   font=('Arial', 10),
                                   width=8)
        self.due_year.pack(side='left', padx=2)
        self.due_year.set(str(current_year))
        
        # Set initial day values
        self.update_day_dropdown()

        # Bind month/year changes to update day dropdown
        self.due_month.bind("<<ComboboxSelected>>", lambda e: self.update_day_dropdown())
        self.due_year.bind("<<ComboboxSelected>>", lambda e: self.update_day_dropdown())
        
        # Status dropdown
        ttk.Label(form_frame, 
                 text="Status:", 
                 background=self.bg_color,
                 foreground=self.text_color,
                 font=('Arial', 10)).grid(row=3, column=0, padx=10, pady=8, sticky='e')
        
        self.assignment_status = ttk.Combobox(form_frame, 
                                            values=["Pending", "In Progress", "Completed"],
                                            font=('Arial', 10),
                                            width=field_width)
        self.assignment_status.grid(row=3, column=1, padx=10, pady=8, sticky='w')
        self.assignment_status.set("Pending")
        
        # Action buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(btn_frame, 
                  text="Add Assignment", 
                  style='Primary.TButton',
                  command=self.add_assignment).pack(side='left', padx=5)
        
        ttk.Button(btn_frame, 
                  text="Update",
                  style='Success.TButton',
                  command=self.update_assignment).pack(side='left', padx=5)
        
        ttk.Button(btn_frame, 
                  text="Delete",
                  style='Danger.TButton',
                  command=self.delete_assignment).pack(side='left', padx=5)
        
        ttk.Button(btn_frame, 
                  text="Clear",
                  style='Secondary.TButton',
                  command=self.clear_assignment_form).pack(side='left', padx=5)
        
        # Assignments list
        list_frame = ttk.LabelFrame(self.content, 
                                  text="Current Assignments",
                                  padding=(15, 10, 15, 15))
        list_frame.pack(fill='both', expand=True)
        
        # Treeview
        columns = ("No", "Subject", "Assignment", "Due Date", "Status")
        self.assignment_tree = ttk.Treeview(list_frame, 
                                          columns=columns, 
                                          show="headings")
        
        # Configure columns
        col_widths = [60, 150, 250, 120, 100]
        for col, width in zip(columns, col_widths):
            self.assignment_tree.heading(col, text=col)
            self.assignment_tree.column(col, width=width, anchor='center')
        
        self.assignment_tree.column("Subject", anchor='w')
        self.assignment_tree.column("Assignment", anchor='w')
        
        # Add scrollbar
        v_scroll = ttk.Scrollbar(list_frame, 
                                orient="vertical", 
                                command=self.assignment_tree.yview)
        self.assignment_tree.configure(yscrollcommand=v_scroll.set)
        
        # Grid layout
        self.assignment_tree.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        
        # Configure frame grid
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Add data sorted by due date
        sorted_assignments = sorted(
            self.assignments,
            key=lambda x: datetime.strptime(x['due_date'], "%d-%m-%Y")
        )
        
        for i, assignment in enumerate(sorted_assignments, start=1):  # Add numbering
            course_name = assignment['course']
            course_code = next(
                (course['code'] for course in self.courses 
                if course['name'] == course_name),
                course_name  # fallback if not found
            )
            display_text = f"[{course_code}] {course_name}"

            self.assignment_tree.insert("", "end", values=(
                i,  # Replace assignment['id'] with numbering
                display_text,
                assignment['title'],
                assignment['due_date'],
                assignment['status']
            ))
        
        # Bind selection to populate form
        self.assignment_tree.bind("<<TreeviewSelect>>", self.populate_assignment_form)
        
        # Auto-save when switching views
        self.save_data()
    
    def update_day_dropdown(self):
        """Update the day dropdown based on selected month and year"""
        try:
            month = int(self.due_month.get())
            year = int(self.due_year.get())
            _, num_days = monthrange(year, month)
            
            days = [f"{d:02d}" for d in range(1, num_days + 1)]
            current_day = self.due_day.get()
            
            self.due_day['values'] = days
            
            # Try to maintain the current selection if valid
            if current_day in days:
                self.due_day.set(current_day)
            else:
                self.due_day.set(days[0])
        except:
            pass
    
    def clear_content(self):
        """Clear the content area"""
        for widget in self.content.winfo_children():
            widget.destroy()
    
    # Course Management Methods
    def add_course(self):
        """Add a new course"""
        code = self.course_code.get().strip().upper()
        name = self.course_name.get().strip()
        
        if not code or not name:
            messagebox.showwarning("Warning", "Please fill in all fields")
            return
        
        # Check if subject code already exists
        if any(course['code'] == code for course in self.courses):
            messagebox.showwarning("Warning", "Subject code already exists")
            return
        
        self.courses.append({
            'code': code,
            'name': name
        })
        
        self.course_tree.insert("", "end", values=(code, name))
        self.clear_course_form()
        messagebox.showinfo("Success", "Subject added successfully")
        self.save_data()
    
    def update_course(self):
        """Update an existing course"""
        selected = self.course_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a course to update")
            return
        
        code = self.course_code.get().strip().upper()
        name = self.course_name.get().strip()
        
        if not code or not name:
            messagebox.showwarning("Warning", "Please fill in all fields")
            return
        
        # Find and update the course
        for course in self.courses:
            if course['code'] == self.course_tree.item(selected)['values'][0]:
                course['code'] = code
                course['name'] = name
                break
        
        # Update the treeview
        self.course_tree.item(selected, values=(code, name))
        self.clear_course_form()
        messagebox.showinfo("Success", "Subject updated successfully")
        self.save_data()
    
    def delete_course(self):
        """Delete a course"""
        selected = self.course_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a course to delete")
            return
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm", "Delete this course and all its assignments?"):
            return
        
        course_code = self.course_tree.item(selected)['values'][0]
        
        # Remove course
        self.courses = [course for course in self.courses if course['code'] != course_code]
        
        # Remove assignments for this course
        self.assignments = [a for a in self.assignments if a['course'] != course_code]
        
        # Update UI
        self.course_tree.delete(selected)
        self.clear_course_form()
        messagebox.showinfo("Success", "Subject deleted successfully")
        self.save_data()
    
    def clear_course_form(self):
        """Clear the course form"""
        self.course_code.delete(0, tk.END)
        self.course_name.delete(0, tk.END)
    
    def populate_course_form(self, event):
        """Populate form with selected course data"""
        selected = self.course_tree.selection()
        if not selected:
            return
        
        values = self.course_tree.item(selected)['values']
        self.clear_course_form()
        
        self.course_code.insert(0, values[0])
        self.course_name.insert(0, values[1])
    
    # Assignment Management Methods
    def add_assignment(self):
        """Add a new assignment"""
        course = self.assignment_course.get().strip()
        title = self.assignment_title.get().strip()
        due_date = f"{self.due_day.get()}-{self.due_month.get()}-{self.due_year.get()}"
        status = self.assignment_status.get().strip()
        
        if not all([course, title, due_date, status]):
            messagebox.showwarning("Warning", "Please fill in all fields")
            return
        
        # Validate date
        try:
            datetime.strptime(due_date, "%d-%m-%Y")
        except ValueError:
            messagebox.showwarning("Warning", "Invalid date selected")
            return
        
        # Generate new ID
        new_id = max([a['id'] for a in self.assignments], default=0) + 1
        
        self.assignments.append({
            'id': new_id,
            'course': course,
            'title': title,
            'due_date': due_date,
            'status': status
        })
        
        self.assignment_tree.insert("", "end", values=(new_id, course, title, due_date, status))
        self.clear_assignment_form()
        messagebox.showinfo("Success", "Assignment added successfully")
        self.save_data()
    
    def update_assignment(self):
        """Update an existing assignment"""
        selected = self.assignment_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an assignment to update")
            return
        
        assignment_id = int(self.assignment_tree.item(selected)['values'][0])
        course = self.assignment_course.get().strip()
        title = self.assignment_title.get().strip()
        due_date = f"{self.due_day.get()}-{self.due_month.get()}-{self.due_year.get()}"
        status = self.assignment_status.get().strip()
        
        if not all([course, title, due_date, status]):
            messagebox.showwarning("Warning", "Please fill in all fields")
            return
        
        # Validate date
        try:
            datetime.strptime(due_date, "%d-%m-%Y")
        except ValueError:
            messagebox.showwarning("Warning", "Invalid date selected")
            return
        
        # Find and update the assignment
        for assignment in self.assignments:
            if assignment['id'] == assignment_id:
                assignment.update({
                    'course': course,
                    'title': title,
                    'due_date': due_date,
                    'status': status
                })
                break
        
        # Update the treeview
        self.assignment_tree.item(selected, values=(assignment_id, course, title, due_date, status))
        self.clear_assignment_form()
        messagebox.showinfo("Success", "Assignment updated successfully")
        self.save_data()
    
    def delete_assignment(self):
        """Delete an assignment"""
        selected = self.assignment_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an assignment to delete")
            return
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm", "Delete this assignment?"):
            return
        
        assignment_id = int(self.assignment_tree.item(selected)['values'][0])
        
        # Remove assignment
        self.assignments = [a for a in self.assignments if a['id'] != assignment_id]
        
        # Update UI
        self.assignment_tree.delete(selected)
        self.clear_assignment_form()
        messagebox.showinfo("Success", "Assignment deleted successfully")
        self.save_data()
    
    def clear_assignment_form(self):
        """Clear the assignment form"""
        self.assignment_course.set('')
        self.assignment_title.delete(0, tk.END)
        
        # Reset date to current date
        today = datetime.now()
        self.due_year.set(str(today.year))
        self.due_month.set(f"{today.month:02d}")
        self.update_day_dropdown()
        self.due_day.set(f"{today.day:02d}")
        
        self.assignment_status.set("Pending")
    
    def populate_assignment_form(self, event):
        """Populate form with selected assignment data"""
        selected = self.assignment_tree.selection()
        if not selected:
            return
        
        values = self.assignment_tree.item(selected)['values']
        self.clear_assignment_form()
        
        self.assignment_course.set(values[1])
        self.assignment_title.insert(0, values[2])
        
        # Parse the due date into year, month, day
        try:
            due_date = values[3]
            day, month, year = due_date.split('-')
            self.due_day.set(day)
            self.due_month.set(month)
            self.due_year.set(year)
            self.update_day_dropdown()
        except:
            pass
        
        self.assignment_status.set(values[4])

    def export_assignments(self):
        file = filedialog.asksaveasfilename(defaultextension=".csv",
                                            filetypes=[("CSV files", "*.csv")])
        if file:
            with open(file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Subject", "Title", "Due Date", "Status"])
                for a in self.assignments:
                    writer.writerow([a['id'], a['course'], a['title'], a['due_date'], a['status']])
            messagebox.showinfo("Exported", "Assignments exported successfully.")

    def show_assignment_details(self, event):
        """Show details of a selected assignment"""
        selected = self.tree.selection()
        if not selected:
            return
        
        values = self.tree.item(selected)['values']
        
        # Create a details window
        details = tk.Toplevel(self.root)
        details.title("Assignment Details")
        details.geometry("500x300")
        
        # Frame for content
        content = ttk.Frame(details, padding=20)
        content.pack(fill='both', expand=True)
        
        # Display assignment details
        ttk.Label(content, 
                 text=f"Subject: {values[1]}", 
                 font=('Arial', 12)).pack(anchor='w', pady=5)
        
        ttk.Label(content, 
                 text=f"Assignment: {values[2]}", 
                 font=('Arial', 12, 'bold')).pack(anchor='w', pady=5)
        
        ttk.Label(content, 
                 text=f"Due Date: {values[3]}", 
                 font=('Arial', 12)).pack(anchor='w', pady=5)
        
        ttk.Label(content, 
                 text=f"Status: {values[4]}", 
                 font=('Arial', 12)).pack(anchor='w', pady=5)
        
        # Close button
        ttk.Button(content, 
                  text="Close", 
                  style='Secondary.TButton',
                  command=details.destroy).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = AssignmentManager(root)
    root.mainloop()