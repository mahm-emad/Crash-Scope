import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from datetime import datetime
from dateutil import parser

class TrafficCrashesSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Traffic Accidents Management System")
        self.root.geometry("1400x900")
        
        # Database connection
        self.conn = self.connect_db()
        if not self.conn:
            messagebox.showerror("Error", "Failed to connect to database")
            root.destroy()
            return
        
        # Create notebook (tabs interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)
        
        # Create tabs for each table
        self.create_crashes_tab()
        self.create_people_tab()
        self.create_vehicles_tab()
        
        # Initialize current selection variables
        self.current_crash_id = None
        self.current_person_id = None
        self.current_vehicle_id = None
    
    def connect_db(self):
        try:
            conn = pyodbc.connect(
                "Driver={SQL Server};"
                "Server=DESKTOP-0UDG9MV\ABDO;"
                "Database=Traffic_Crashes;"
                "Trusted_Connection=yes;"
            )
            return conn
        except Exception as e:
            print("Database connection error:", e)
            return None

    def create_crashes_tab(self):
        """Create tab for accident data management with all columns"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Accidents")
        
        # Create paned window for resizable split view
        paned = ttk.PanedWindow(tab, orient=tk.HORIZONTAL)
        paned.pack(fill='both', expand=True)
        
        # Left pane - Form with all fields
        form_frame = ttk.LabelFrame(paned, text="Accident Details (All Fields)")
        paned.add(form_frame, weight=1)
        
        # Create scrollable form
        canvas = tk.Canvas(form_frame)
        scrollbar = ttk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # All fields from Crashes table
        self.crash_entries = {}
        fields = [
            ("CRASH_RECORD_ID", "Crash ID*:", "entry", True),
            ("CRASH_DATE", "Crash Date (YYYY-MM-DD HH:MM):", "entry", False),
            ("POSTED_SPEED_LIMIT", "Posted Speed Limit:", "entry", False),
            ("TRAFFIC_CONTROL_DEVICE", "Traffic Control Device:", "combobox", ["", "Traffic Signal", "Stop Sign", "Yield Sign", "No Controls", "Other"]),
            ("DEVICE_CONDITION", "Device Condition:", "combobox", ["", "Functioning", "Not Functioning", "Missing", "Not Applicable"]),
            ("WEATHER_CONDITION", "Weather Condition:", "combobox", ["", "Clear", "Rain", "Snow", "Fog", "Other"]),
            ("LIGHTING_CONDITION", "Lighting Condition:", "combobox", ["", "Daylight", "Dawn/Dusk", "Dark - Lighted", "Dark - Not Lighted"]),
            ("FIRST_CRASH_TYPE", "First Crash Type:", "combobox", ["", "Rear-End", "Side-Impact", "Head-On", "Fixed Object", "Rollover", "Single Vehicle", "Other"]),
            ("TRAFFICWAY_TYPE", "Trafficway Type:", "combobox", ["", "Two-Way", "One-Way", "Divided Highway", "Intersection", "Other"]),
            ("ALIGNMENT", "Alignment:", "combobox", ["", "Straight", "Curve", "Hillcrest", "Other"]),
            ("ROADWAY_SURFACE_COND", "Roadway Surface Condition:", "combobox", ["", "Dry", "Wet", "Snowy", "Icy", "Other"]),
            ("ROAD_DEFECT", "Road Defect:", "combobox", ["", "None", "Pothole", "Rut", "Bump", "Other"]),
            ("CRASH_TYPE", "Crash Type:", "combobox", ["", "Property Damage", "Injury", "Fatal"]),
            ("DAMAGE", "Damage:", "combobox", ["", "None", "Minor", "Moderate", "Severe", "Totaled"]),
            ("PRIM_CONTRIBUTORY_CAUSE", "Primary Cause:", "combobox", ["", "Speeding", "Distraction", "Failure to Yield", "Lane Deviation", "DUI", "Other"]),
            ("SEC_CONTRIBUTORY_CAUSE", "Secondary Cause:", "combobox", ["", "None", "Speeding", "Distraction", "Failure to Yield", "Other"]),
            ("NUM_UNITS", "Number of Units:", "entry", False),
            ("MOST_SEVERE_INJURY", "Most Severe Injury:", "combobox", ["", "None", "Possible", "Non-Incapacitating", "Incapacitating", "Fatal"]),
            ("INJURIES_TOTAL", "Total Injuries:", "entry", False),
            ("INJURIES_FATAL", "Fatal Injuries:", "entry", False),
            ("CRASH_HOUR", "Crash Hour:", "entry", False, True),  # Readonly
            ("CRASH_DAY_OF_WEEK", "Day of Week:", "entry", False, True),  # Readonly
            ("CRASH_MONTH", "Month:", "entry", False, True),  # Readonly
            ("LATITUDE", "Latitude:", "entry", False),
            ("LONGITUDE", "Longitude:", "entry", False),
            ("CRASH_YEAR", "Year:", "entry", False, True)  # Readonly
        ]
        
        for i, (field, label, field_type, options, *readonly) in enumerate(fields):
            ttk.Label(scrollable_frame, text=label).grid(row=i, column=0, padx=5, pady=2, sticky='e')
            
            if field_type == "combobox":
                entry = ttk.Combobox(scrollable_frame, values=options)
                entry.set("")
            else:
                entry = ttk.Entry(scrollable_frame)
                if readonly and readonly[0]:
                    entry.config(state='readonly')
            
            entry.grid(row=i, column=1, padx=5, pady=2, sticky='ew')
            self.crash_entries[field] = entry
        
        # Set default values for some fields
        now = datetime.now()
        self.crash_entries["CRASH_DATE"].insert(0, now.strftime("%Y-%m-%d %H:%M"))
        self.update_datetime_fields(now)
        
        # Bind CRASH_DATE changes to update the derived fields
        self.crash_entries["CRASH_DATE"].bind("<FocusOut>", self.on_crash_date_changed)
        
        # Button frame
        btn_frame = ttk.Frame(scrollable_frame)
        btn_frame.grid(row=len(fields), columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Add New", command=self.clear_crash_fields).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Save", command=self.save_crash).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_crash).pack(side='left', padx=5)
        
        # Right pane - Data table
        table_frame = ttk.LabelFrame(paned, text="Accidents List")
        paned.add(table_frame, weight=2)
        
        # Treeview with scrollbars
        self.crash_tree = ttk.Treeview(table_frame)
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.crash_tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.crash_tree.xview)
        self.crash_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.crash_tree.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')
        
        # Configure columns
        self.crash_tree['columns'] = ("ID", "Date", "Type", "Primary Cause", "Injuries", "Hour", "Day", "Month", "Year")
        self.crash_tree.column("#0", width=0, stretch=tk.NO)
        self.crash_tree.column("ID", width=100)
        self.crash_tree.column("Date", width=120)
        self.crash_tree.column("Type", width=120)
        self.crash_tree.column("Primary Cause", width=150)
        self.crash_tree.column("Injuries", width=80)
        self.crash_tree.column("Hour", width=60)
        self.crash_tree.column("Day", width=80)
        self.crash_tree.column("Month", width=80)
        self.crash_tree.column("Year", width=60)
        
        self.crash_tree.heading("ID", text="Crash ID")
        self.crash_tree.heading("Date", text="Date")
        self.crash_tree.heading("Type", text="Crash Type")
        self.crash_tree.heading("Primary Cause", text="Primary Cause")
        self.crash_tree.heading("Injuries", text="Injuries")
        self.crash_tree.heading("Hour", text="Hour")
        self.crash_tree.heading("Day", text="Day")
        self.crash_tree.heading("Month", text="Month")
        self.crash_tree.heading("Year", text="Year")
        
        # Bind selection event
        self.crash_tree.bind('<<TreeviewSelect>>', self.on_crash_select)
        
        # Load data
        self.load_crashes()
    
    def on_crash_date_changed(self, event):
        """Update derived datetime fields when crash date changes"""
        try:
            date_str = self.crash_entries["CRASH_DATE"].get()
            if date_str:
                dt = parser.parse(date_str)
                self.update_datetime_fields(dt)
        except ValueError:
            pass
    
    def update_datetime_fields(self, dt):
        """Update the readonly datetime fields based on a datetime object"""
        self.crash_entries["CRASH_HOUR"].config(state='normal')
        self.crash_entries["CRASH_HOUR"].delete(0, tk.END)
        self.crash_entries["CRASH_HOUR"].insert(0, dt.hour)
        self.crash_entries["CRASH_HOUR"].config(state='readonly')
        
        self.crash_entries["CRASH_DAY_OF_WEEK"].config(state='normal')
        self.crash_entries["CRASH_DAY_OF_WEEK"].delete(0, tk.END)
        self.crash_entries["CRASH_DAY_OF_WEEK"].insert(0, dt.strftime("%A"))
        self.crash_entries["CRASH_DAY_OF_WEEK"].config(state='readonly')
        
        self.crash_entries["CRASH_MONTH"].config(state='normal')
        self.crash_entries["CRASH_MONTH"].delete(0, tk.END)
        self.crash_entries["CRASH_MONTH"].insert(0, dt.strftime("%B"))
        self.crash_entries["CRASH_MONTH"].config(state='readonly')
        
        self.crash_entries["CRASH_YEAR"].config(state='normal')
        self.crash_entries["CRASH_YEAR"].delete(0, tk.END)
        self.crash_entries["CRASH_YEAR"].insert(0, dt.year)
        self.crash_entries["CRASH_YEAR"].config(state='readonly')
    
    def create_people_tab(self):
        """Create tab for person data management with all columns"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="People")
        
        # Create paned window for resizable split view
        paned = ttk.PanedWindow(tab, orient=tk.HORIZONTAL)
        paned.pack(fill='both', expand=True)
        
        # Left pane - Form with all fields
        form_frame = ttk.LabelFrame(paned, text="Person Details (All Fields)")
        paned.add(form_frame, weight=1)
        
        # Create scrollable form
        canvas = tk.Canvas(form_frame)
        scrollbar = ttk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # All fields from People table
        self.person_entries = {}
        fields = [
            ("PERSON_ID", "Person ID:", "entry", False),
            ("CRASH_RECORD_ID", "Crash ID*:", "entry", True),
            ("PERSON_TYPE", "Person Type:", "combobox", ["", "Driver", "Passenger", "Pedestrian"]),
            ("VEHICLE_ID", "Vehicle ID:", "entry", False),
            ("CRASH_DATE", "Crash Date:", "entry", False),
            ("SEX", "Gender:", "combobox", ["", "Male", "Female"]),
            ("AGE", "Age:", "entry", False),
            ("DRIVERS_LICENSE_STATE", "License State:", "entry", False),
            ("DRIVERS_LICENSE_CLASS", "License Class:", "entry", False),
            ("SAFETY_EQUIPMENT", "Safety Equipment:", "combobox", ["", "None", "Seat Belt", "Helmet", "Child Seat", "Other"]),
            ("AIRBAG_DEPLOYED", "Airbag Deployed:", "combobox", ["", "Yes", "No", "Not Applicable"]),
            ("EJECTION", "Ejection:", "combobox", ["", "None", "Partial", "Complete"]),
            ("INJURY_CLASSIFICATION", "Injury Classification:", "combobox", ["", "No Injury", "Possible", "Non-Incapacitating", "Incapacitating", "Fatal"]),
            ("DRIVER_ACTION", "Driver Action:", "combobox", ["", "None", "Braking", "Accelerating", "Turning", "Other"]),
            ("PHYSICAL_CONDITION", "Physical Condition:", "combobox", ["", "Normal", "Fatigued", "Ill", "Impaired", "Other"]),
            ("BAC_RESULT", "BAC Result:", "entry", False)
        ]
        
        for i, (field, label, field_type, options) in enumerate(fields):
            ttk.Label(scrollable_frame, text=label).grid(row=i, column=0, padx=5, pady=2, sticky='e')
            
            if field_type == "combobox":
                entry = ttk.Combobox(scrollable_frame, values=options)
                entry.set("")
            else:
                entry = ttk.Entry(scrollable_frame)
            
            entry.grid(row=i, column=1, padx=5, pady=2, sticky='ew')
            self.person_entries[field] = entry
        
        # Button frame
        btn_frame = ttk.Frame(scrollable_frame)
        btn_frame.grid(row=len(fields), columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Add New", command=self.clear_person_fields).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Save", command=self.save_person).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_person).pack(side='left', padx=5)
        
        # Right pane - Data table
        table_frame = ttk.LabelFrame(paned, text="People List")
        paned.add(table_frame, weight=2)
        
        # Treeview with scrollbars
        self.person_tree = ttk.Treeview(table_frame)
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.person_tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.person_tree.xview)
        self.person_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.person_tree.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')
        
        # Configure columns
        self.person_tree['columns'] = ("ID", "Crash ID", "Type", "Gender", "Age", "Injury", "Crash Date")
        self.person_tree.column("#0", width=0, stretch=tk.NO)
        self.person_tree.column("ID", width=80)
        self.person_tree.column("Crash ID", width=100)
        self.person_tree.column("Type", width=100)
        self.person_tree.column("Gender", width=80)
        self.person_tree.column("Age", width=60)
        self.person_tree.column("Injury", width=120)
        self.person_tree.column("Crash Date", width=120)
        
        self.person_tree.heading("ID", text="Person ID")
        self.person_tree.heading("Crash ID", text="Crash ID")
        self.person_tree.heading("Type", text="Type")
        self.person_tree.heading("Gender", text="Gender")
        self.person_tree.heading("Age", text="Age")
        self.person_tree.heading("Injury", text="Injury Level")
        self.person_tree.heading("Crash Date", text="Crash Date")
        
        # Bind selection event
        self.person_tree.bind('<<TreeviewSelect>>', self.on_person_select)
        
        # Load data
        self.load_people()
    
    def create_vehicles_tab(self):
        """Create tab for vehicle data management with all columns"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Vehicles")
        
        # Create paned window for resizable split view
        paned = ttk.PanedWindow(tab, orient=tk.HORIZONTAL)
        paned.pack(fill='both', expand=True)
        
        # Left pane - Form with all fields
        form_frame = ttk.LabelFrame(paned, text="Vehicle Details (All Fields)")
        paned.add(form_frame, weight=1)
        
        # Create scrollable form
        canvas = tk.Canvas(form_frame)
        scrollbar = ttk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # All fields from Vehicles table
        self.vehicle_entries = {}
        fields = [
            ("Crash_Unit_ID", "Unit ID:", "entry", False),
            ("CRASH_RECORD_ID", "Crash ID*:", "entry", True),
            ("CRASH_DATE", "Crash Date:", "entry", False),
            ("Unit_No", "Unit Number:", "entry", False),
            ("Unit_Type", "Unit Type:", "combobox", ["", "Car", "Truck", "Motorcycle", "Bus", "Bicycle", "Other"]),
            ("VEHICLE_ID", "Vehicle ID:", "entry", False),
            ("Make", "Make:", "entry", False),
            ("Model", "Model:", "entry", False),
            ("Lic_Plate_State", "License State:", "entry", False),
            ("Vehicle_Year", "Year:", "entry", False),
            ("Vehicle_Defect", "Vehicle Defect:", "combobox", ["", "None", "Brakes", "Lights", "Tires", "Other"]),
            ("Vehicle_Type", "Vehicle Type:", "combobox", ["", "Passenger", "Commercial", "Emergency", "Government", "Other"]),
            ("Vehicle_Use", "Vehicle Use:", "combobox", ["", "Personal", "Commercial", "Rental", "Taxi", "Other"]),
            ("Travel_direction", "Travel Direction:", "combobox", ["", "North", "South", "East", "West", "Other"]),
            ("maneuver", "Maneuver:", "combobox", ["", "Straight", "Turning", "Changing Lanes", "Stopped", "Other"]),
            ("Occupant_CNT", "Occupant Count:", "entry", False),
            ("First_contact_point", "First Contact Point:", "combobox", ["", "Front", "Rear", "Side", "Top", "Undercarriage", "Other"])
        ]
        
        for i, (field, label, field_type, options) in enumerate(fields):
            ttk.Label(scrollable_frame, text=label).grid(row=i, column=0, padx=5, pady=2, sticky='e')
            
            if field_type == "combobox":
                entry = ttk.Combobox(scrollable_frame, values=options)
                entry.set("")
            else:
                entry = ttk.Entry(scrollable_frame)
            
            entry.grid(row=i, column=1, padx=5, pady=2, sticky='ew')
            self.vehicle_entries[field] = entry
        
        # Button frame
        btn_frame = ttk.Frame(scrollable_frame)
        btn_frame.grid(row=len(fields), columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Add New", command=self.clear_vehicle_fields).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Save", command=self.save_vehicle).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_vehicle).pack(side='left', padx=5)
        
        # Right pane - Data table
        table_frame = ttk.LabelFrame(paned, text="Vehicles List")
        paned.add(table_frame, weight=2)
        
        # Treeview with scrollbars
        self.vehicle_tree = ttk.Treeview(table_frame)
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.vehicle_tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.vehicle_tree.xview)
        self.vehicle_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.vehicle_tree.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')
        
        # Configure columns
        self.vehicle_tree['columns'] = ("Unit ID", "Crash ID", "Type", "Make", "Model", "Year", "Crash Date")
        self.vehicle_tree.column("#0", width=0, stretch=tk.NO)
        self.vehicle_tree.column("Unit ID", width=80)
        self.vehicle_tree.column("Crash ID", width=100)
        self.vehicle_tree.column("Type", width=100)
        self.vehicle_tree.column("Make", width=120)
        self.vehicle_tree.column("Model", width=120)
        self.vehicle_tree.column("Year", width=60)
        self.vehicle_tree.column("Crash Date", width=120)
        
        self.vehicle_tree.heading("Unit ID", text="Unit ID")
        self.vehicle_tree.heading("Crash ID", text="Crash ID")
        self.vehicle_tree.heading("Type", text="Type")
        self.vehicle_tree.heading("Make", text="Make")
        self.vehicle_tree.heading("Model", text="Model")
        self.vehicle_tree.heading("Year", text="Year")
        self.vehicle_tree.heading("Crash Date", text="Crash Date")
        
        # Bind selection event
        self.vehicle_tree.bind('<<TreeviewSelect>>', self.on_vehicle_select)
        
        # Load data
        self.load_vehicles()
    
    def load_crashes(self):
        """Load accident data into the treeview with datetime fields"""
        try:
            # Clear existing data
            for item in self.crash_tree.get_children():
                self.crash_tree.delete(item)
            
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT CRASH_RECORD_ID, CRASH_DATE, FIRST_CRASH_TYPE, 
                       PRIM_CONTRIBUTORY_CAUSE, INJURIES_TOTAL
                FROM Crashes
                """)
            
            for row in cursor.fetchall():
                date_str = row.CRASH_DATE.strftime("%Y-%m-%d %H:%M") if row.CRASH_DATE else ""
                hour = row.CRASH_DATE.hour if row.CRASH_DATE else ""
                day = row.CRASH_DATE.strftime("%A") if row.CRASH_DATE else ""
                month = row.CRASH_DATE.strftime("%B") if row.CRASH_DATE else ""
                year = row.CRASH_DATE.year if row.CRASH_DATE else ""
                
                self.crash_tree.insert("", "end", values=(
                    row.CRASH_RECORD_ID,
                    date_str,
                    row.FIRST_CRASH_TYPE,
                    row.PRIM_CONTRIBUTORY_CAUSE,
                    row.INJURIES_TOTAL,
                    hour,
                    day,
                    month,
                    year
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load accident data: {str(e)}")
    
    def on_crash_select(self, event):
        """Handle selection of an accident record and load all fields"""
        selected = self.crash_tree.focus()
        if not selected:
            return
        
        values = self.crash_tree.item(selected, 'values')
        if not values:
            return
        
        self.current_crash_id = values[0]
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Crashes WHERE CRASH_RECORD_ID=?", self.current_crash_id)
            row = cursor.fetchone()
            
            if row:
                for field, entry in self.crash_entries.items():
                    value = getattr(row, field)
                    if value is None:
                        value = ""
                    
                    if isinstance(entry, ttk.Combobox):
                        entry.set(str(value))
                    else:
                        entry.config(state='normal')
                        entry.delete(0, tk.END)
                        if field == "CRASH_DATE" and value:
                            entry.insert(0, value.strftime("%Y-%m-%d %H:%M"))
                            # Update derived fields
                            self.update_datetime_fields(value)
                        else:
                            entry.insert(0, str(value))
                        
                        if field in ["CRASH_HOUR", "CRASH_DAY_OF_WEEK", "CRASH_MONTH", "CRASH_YEAR"]:
                            entry.config(state='readonly')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load accident details: {str(e)}")
    
    def save_crash(self):
        """Save or update accident data with all fields"""
        if not self.crash_entries["CRASH_RECORD_ID"].get():
            messagebox.showwarning("Warning", "Crash ID is required")
            return
        
        try:
            # Parse the datetime string
            crash_date_str = self.crash_entries["CRASH_DATE"].get()
            crash_date = parser.parse(crash_date_str) if crash_date_str else None
            
            cursor = self.conn.cursor()
            
            if self.current_crash_id:  # Update existing record
                cursor.execute(
                    """
                    UPDATE Crashes SET 
                        CRASH_DATE=?, POSTED_SPEED_LIMIT=?, TRAFFIC_CONTROL_DEVICE=?,
                        DEVICE_CONDITION=?, WEATHER_CONDITION=?, LIGHTING_CONDITION=?,
                        FIRST_CRASH_TYPE=?, TRAFFICWAY_TYPE=?, ALIGNMENT=?,
                        ROADWAY_SURFACE_COND=?, ROAD_DEFECT=?, CRASH_TYPE=?,
                        DAMAGE=?, PRIM_CONTRIBUTORY_CAUSE=?, SEC_CONTRIBUTORY_CAUSE=?,
                        NUM_UNITS=?, MOST_SEVERE_INJURY=?, INJURIES_TOTAL=?,
                        INJURIES_FATAL=?, CRASH_HOUR=?, CRASH_DAY_OF_WEEK=?,
                        CRASH_MONTH=?, LATITUDE=?, LONGITUDE=?, CRASH_YEAR=?
                    WHERE CRASH_RECORD_ID=?
                    """,
                    crash_date,
                    int(self.crash_entries["POSTED_SPEED_LIMIT"].get()) if self.crash_entries["POSTED_SPEED_LIMIT"].get() else None,
                    self.crash_entries["TRAFFIC_CONTROL_DEVICE"].get(),
                    self.crash_entries["DEVICE_CONDITION"].get(),
                    self.crash_entries["WEATHER_CONDITION"].get(),
                    self.crash_entries["LIGHTING_CONDITION"].get(),
                    self.crash_entries["FIRST_CRASH_TYPE"].get(),
                    self.crash_entries["TRAFFICWAY_TYPE"].get(),
                    self.crash_entries["ALIGNMENT"].get(),
                    self.crash_entries["ROADWAY_SURFACE_COND"].get(),
                    self.crash_entries["ROAD_DEFECT"].get(),
                    self.crash_entries["CRASH_TYPE"].get(),
                    self.crash_entries["DAMAGE"].get(),
                    self.crash_entries["PRIM_CONTRIBUTORY_CAUSE"].get(),
                    self.crash_entries["SEC_CONTRIBUTORY_CAUSE"].get(),
                    int(self.crash_entries["NUM_UNITS"].get()) if self.crash_entries["NUM_UNITS"].get() else None,
                    self.crash_entries["MOST_SEVERE_INJURY"].get(),
                    int(self.crash_entries["INJURIES_TOTAL"].get()) if self.crash_entries["INJURIES_TOTAL"].get() else None,
                    int(self.crash_entries["INJURIES_FATAL"].get()) if self.crash_entries["INJURIES_FATAL"].get() else None,
                    int(self.crash_entries["CRASH_HOUR"].get()) if self.crash_entries["CRASH_HOUR"].get() else None,
                    self.crash_entries["CRASH_DAY_OF_WEEK"].get(),
                    self.crash_entries["CRASH_MONTH"].get(),
                    float(self.crash_entries["LATITUDE"].get()) if self.crash_entries["LATITUDE"].get() else None,
                    float(self.crash_entries["LONGITUDE"].get()) if self.crash_entries["LONGITUDE"].get() else None,
                    int(self.crash_entries["CRASH_YEAR"].get()) if self.crash_entries["CRASH_YEAR"].get() else None,
                    self.crash_entries["CRASH_RECORD_ID"].get()
                )
                message = "Accident data updated successfully"
            else:  # Insert new record
                cursor.execute(
                    """
                    INSERT INTO Crashes (
                        CRASH_RECORD_ID, CRASH_DATE, POSTED_SPEED_LIMIT, TRAFFIC_CONTROL_DEVICE,
                        DEVICE_CONDITION, WEATHER_CONDITION, LIGHTING_CONDITION,
                        FIRST_CRASH_TYPE, TRAFFICWAY_TYPE, ALIGNMENT,
                        ROADWAY_SURFACE_COND, ROAD_DEFECT, CRASH_TYPE,
                        DAMAGE, PRIM_CONTRIBUTORY_CAUSE, SEC_CONTRIBUTORY_CAUSE,
                        NUM_UNITS, MOST_SEVERE_INJURY, INJURIES_TOTAL,
                        INJURIES_FATAL, CRASH_HOUR, CRASH_DAY_OF_WEEK,
                        CRASH_MONTH, LATITUDE, LONGITUDE, CRASH_YEAR
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    self.crash_entries["CRASH_RECORD_ID"].get(),
                    crash_date,
                    int(self.crash_entries["POSTED_SPEED_LIMIT"].get()) if self.crash_entries["POSTED_SPEED_LIMIT"].get() else None,
                    self.crash_entries["TRAFFIC_CONTROL_DEVICE"].get(),
                    self.crash_entries["DEVICE_CONDITION"].get(),
                    self.crash_entries["WEATHER_CONDITION"].get(),
                    self.crash_entries["LIGHTING_CONDITION"].get(),
                    self.crash_entries["FIRST_CRASH_TYPE"].get(),
                    self.crash_entries["TRAFFICWAY_TYPE"].get(),
                    self.crash_entries["ALIGNMENT"].get(),
                    self.crash_entries["ROADWAY_SURFACE_COND"].get(),
                    self.crash_entries["ROAD_DEFECT"].get(),
                    self.crash_entries["CRASH_TYPE"].get(),
                    self.crash_entries["DAMAGE"].get(),
                    self.crash_entries["PRIM_CONTRIBUTORY_CAUSE"].get(),
                    self.crash_entries["SEC_CONTRIBUTORY_CAUSE"].get(),
                    int(self.crash_entries["NUM_UNITS"].get()) if self.crash_entries["NUM_UNITS"].get() else None,
                    self.crash_entries["MOST_SEVERE_INJURY"].get(),
                    int(self.crash_entries["INJURIES_TOTAL"].get()) if self.crash_entries["INJURIES_TOTAL"].get() else None,
                    int(self.crash_entries["INJURIES_FATAL"].get()) if self.crash_entries["INJURIES_FATAL"].get() else None,
                    int(self.crash_entries["CRASH_HOUR"].get()) if self.crash_entries["CRASH_HOUR"].get() else None,
                    self.crash_entries["CRASH_DAY_OF_WEEK"].get(),
                    self.crash_entries["CRASH_MONTH"].get(),
                    float(self.crash_entries["LATITUDE"].get()) if self.crash_entries["LATITUDE"].get() else None,
                    float(self.crash_entries["LONGITUDE"].get()) if self.crash_entries["LONGITUDE"].get() else None,
                    int(self.crash_entries["CRASH_YEAR"].get()) if self.crash_entries["CRASH_YEAR"].get() else None
                )
                message = "Accident data saved successfully"
            
            self.conn.commit()
            messagebox.showinfo("Success", message)
            self.load_crashes()
            self.clear_crash_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")
    
    def clear_crash_fields(self):
        """Clear all accident form fields"""
        self.current_crash_id = None
        for field, entry in self.crash_entries.items():
            if isinstance(entry, ttk.Combobox):
                entry.set("")
            else:
                entry.config(state='normal')
                entry.delete(0, tk.END)
                if field in ["CRASH_HOUR", "CRASH_DAY_OF_WEEK", "CRASH_MONTH", "CRASH_YEAR"]:
                    entry.config(state='readonly')
        
        # Set default values for some fields
        now = datetime.now()
        self.crash_entries["CRASH_DATE"].insert(0, now.strftime("%Y-%m-%d %H:%M"))
        self.update_datetime_fields(now)
    
    def load_people(self):
        """Load person data into the treeview"""
        try:
            # Clear existing data
            for item in self.person_tree.get_children():
                self.person_tree.delete(item)
            
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT p.PERSON_ID, p.CRASH_RECORD_ID, p.PERSON_TYPE, p.SEX, p.AGE, 
                       p.INJURY_CLASSIFICATION, c.CRASH_DATE
                FROM People p
                LEFT JOIN Crashes c ON p.CRASH_RECORD_ID = c.CRASH_RECORD_ID
                """)
            
            for row in cursor.fetchall():
                crash_date = row.CRASH_DATE.strftime("%Y-%m-%d %H:%M") if row.CRASH_DATE else ""
                self.person_tree.insert("", "end", values=(
                    row.PERSON_ID,
                    row.CRASH_RECORD_ID,
                    row.PERSON_TYPE,
                    row.SEX,
                    row.AGE,
                    row.INJURY_CLASSIFICATION,
                    crash_date
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load people data: {str(e)}")
    
    def on_person_select(self, event):
        """Handle selection of a person record and load all fields"""
        selected = self.person_tree.focus()
        if not selected:
            return
        
        values = self.person_tree.item(selected, 'values')
        if not values:
            return
        
        self.current_person_id = values[0]
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM People WHERE PERSON_ID=?", self.current_person_id)
            row = cursor.fetchone()
            
            if row:
                for field, entry in self.person_entries.items():
                    value = getattr(row, field)
                    if value is None:
                        value = ""
                    
                    if isinstance(entry, ttk.Combobox):
                        entry.set(str(value))
                    else:
                        entry.delete(0, tk.END)
                        if field == "CRASH_DATE" and value:
                            entry.insert(0, value.strftime("%Y-%m-%d %H:%M"))
                        else:
                            entry.insert(0, str(value))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load person details: {str(e)}")
    
    def save_person(self):
        """Save or update person data with all fields"""
        if not self.person_entries["CRASH_RECORD_ID"].get():
            messagebox.showwarning("Warning", "Crash ID is required")
            return
        
        try:
            cursor = self.conn.cursor()
            
            # Parse the datetime string if exists
            crash_date_str = self.person_entries["CRASH_DATE"].get()
            crash_date = parser.parse(crash_date_str) if crash_date_str else None
            
            if self.current_person_id:  # Update existing record
                cursor.execute(
                    """
                    UPDATE People SET 
                        PERSON_TYPE=?, CRASH_RECORD_ID=?, VEHICLE_ID=?,
                        CRASH_DATE=?, SEX=?, AGE=?,
                        DRIVERS_LICENSE_STATE=?, DRIVERS_LICENSE_CLASS=?,
                        SAFETY_EQUIPMENT=?, AIRBAG_DEPLOYED=?, EJECTION=?,
                        INJURY_CLASSIFICATION=?, DRIVER_ACTION=?, PHYSICAL_CONDITION=?,
                        BAC_RESULT=?
                    WHERE PERSON_ID=?
                    """,
                    self.person_entries["PERSON_TYPE"].get(),
                    self.person_entries["CRASH_RECORD_ID"].get(),
                    self.person_entries["VEHICLE_ID"].get(),
                    crash_date,
                    self.person_entries["SEX"].get(),
                    int(self.person_entries["AGE"].get()) if self.person_entries["AGE"].get() else None,
                    self.person_entries["DRIVERS_LICENSE_STATE"].get(),
                    self.person_entries["DRIVERS_LICENSE_CLASS"].get(),
                    self.person_entries["SAFETY_EQUIPMENT"].get(),
                    self.person_entries["AIRBAG_DEPLOYED"].get(),
                    self.person_entries["EJECTION"].get(),
                    self.person_entries["INJURY_CLASSIFICATION"].get(),
                    self.person_entries["DRIVER_ACTION"].get(),
                    self.person_entries["PHYSICAL_CONDITION"].get(),
                    self.person_entries["BAC_RESULT"].get(),
                    self.current_person_id
                )
                message = "Person data updated successfully"
            else:  # Insert new record
                cursor.execute(
                    """
                    INSERT INTO People (
                        PERSON_ID, PERSON_TYPE, CRASH_RECORD_ID, VEHICLE_ID,
                        CRASH_DATE, SEX, AGE,
                        DRIVERS_LICENSE_STATE, DRIVERS_LICENSE_CLASS,
                        SAFETY_EQUIPMENT, AIRBAG_DEPLOYED, EJECTION,
                        INJURY_CLASSIFICATION, DRIVER_ACTION, PHYSICAL_CONDITION,
                        BAC_RESULT
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    int(self.person_entries["PERSON_ID"].get()) if self.person_entries["PERSON_ID"].get() else None,
                    self.person_entries["PERSON_TYPE"].get(),
                    self.person_entries["CRASH_RECORD_ID"].get(),
                    self.person_entries["VEHICLE_ID"].get(),
                    crash_date,
                    self.person_entries["SEX"].get(),
                    int(self.person_entries["AGE"].get()) if self.person_entries["AGE"].get() else None,
                    self.person_entries["DRIVERS_LICENSE_STATE"].get(),
                    self.person_entries["DRIVERS_LICENSE_CLASS"].get(),
                    self.person_entries["SAFETY_EQUIPMENT"].get(),
                    self.person_entries["AIRBAG_DEPLOYED"].get(),
                    self.person_entries["EJECTION"].get(),
                    self.person_entries["INJURY_CLASSIFICATION"].get(),
                    self.person_entries["DRIVER_ACTION"].get(),
                    self.person_entries["PHYSICAL_CONDITION"].get(),
                    self.person_entries["BAC_RESULT"].get()
                )
                message = "Person data saved successfully"
            
            self.conn.commit()
            messagebox.showinfo("Success", message)
            self.load_people()
            self.clear_person_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")
    
    def clear_person_fields(self):
        """Clear all person form fields"""
        self.current_person_id = None
        for field, entry in self.person_entries.items():
            if isinstance(entry, ttk.Combobox):
                entry.set("")
            else:
                entry.delete(0, tk.END)
    
    def load_vehicles(self):
        """Load vehicle data into the treeview"""
        try:
            # Clear existing data
            for item in self.vehicle_tree.get_children():
                self.vehicle_tree.delete(item)
            
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT v.Crash_Unit_ID, v.CRASH_RECORD_ID, v.Unit_Type, 
                       v.Make, v.Model, v.Vehicle_Year, c.CRASH_DATE
                FROM Vehicles v
                LEFT JOIN Crashes c ON v.CRASH_RECORD_ID = c.CRASH_RECORD_ID
                """)
            
            for row in cursor.fetchall():
                crash_date = row.CRASH_DATE.strftime("%Y-%m-%d %H:%M") if row.CRASH_DATE else ""
                self.vehicle_tree.insert("", "end", values=(
                    row.Crash_Unit_ID,
                    row.CRASH_RECORD_ID,
                    row.Unit_Type,
                    row.Make,
                    row.Model,
                    row.Vehicle_Year,
                    crash_date
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load vehicle data: {str(e)}")
    
    def on_vehicle_select(self, event):
        """Handle selection of a vehicle record and load all fields"""
        selected = self.vehicle_tree.focus()
        if not selected:
            return
        
        values = self.vehicle_tree.item(selected, 'values')
        if not values:
            return
        
        self.current_vehicle_id = values[0]
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Vehicles WHERE Crash_Unit_ID=?", self.current_vehicle_id)
            row = cursor.fetchone()
            
            if row:
                for field, entry in self.vehicle_entries.items():
                    value = getattr(row, field)
                    if value is None:
                        value = ""
                    
                    if isinstance(entry, ttk.Combobox):
                        entry.set(str(value))
                    else:
                        entry.delete(0, tk.END)
                        if field == "CRASH_DATE" and value:
                            entry.insert(0, value.strftime("%Y-%m-%d %H:%M"))
                        else:
                            entry.insert(0, str(value))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load vehicle details: {str(e)}")
    
    def save_vehicle(self):
        """Save or update vehicle data with all fields"""
        if not self.vehicle_entries["CRASH_RECORD_ID"].get():
            messagebox.showwarning("Warning", "Crash ID is required")
            return
        
        try:
            cursor = self.conn.cursor()
            
            # Parse the datetime string if exists
            crash_date_str = self.vehicle_entries["CRASH_DATE"].get()
            crash_date = parser.parse(crash_date_str) if crash_date_str else None
            
            if self.current_vehicle_id:  # Update existing record
                cursor.execute(
                    """
                    UPDATE Vehicles SET 
                        CRASH_RECORD_ID=?, CRASH_DATE=?, Unit_No=?,
                        Unit_Type=?, VEHICLE_ID=?, Make=?,
                        Model=?, Lic_Plate_State=?, Vehicle_Year=?,
                        Vehicle_Defect=?, Vehicle_Type=?, Vehicle_Use=?,
                        Travel_direction=?, maneuver=?, Occupant_CNT=?,
                        First_contact_point=?
                    WHERE Crash_Unit_ID=?
                    """,
                    self.vehicle_entries["CRASH_RECORD_ID"].get(),
                    crash_date,
                    int(self.vehicle_entries["Unit_No"].get()) if self.vehicle_entries["Unit_No"].get() else None,
                    self.vehicle_entries["Unit_Type"].get(),
                    int(self.vehicle_entries["VEHICLE_ID"].get()) if self.vehicle_entries["VEHICLE_ID"].get() else None,
                    self.vehicle_entries["Make"].get(),
                    self.vehicle_entries["Model"].get(),
                    self.vehicle_entries["Lic_Plate_State"].get(),
                    int(self.vehicle_entries["Vehicle_Year"].get()) if self.vehicle_entries["Vehicle_Year"].get() else None,
                    self.vehicle_entries["Vehicle_Defect"].get(),
                    self.vehicle_entries["Vehicle_Type"].get(),
                    self.vehicle_entries["Vehicle_Use"].get(),
                    self.vehicle_entries["Travel_direction"].get(),
                    self.vehicle_entries["maneuver"].get(),
                    int(self.vehicle_entries["Occupant_CNT"].get()) if self.vehicle_entries["Occupant_CNT"].get() else None,
                    self.vehicle_entries["First_contact_point"].get(),
                    self.current_vehicle_id
                )
                message = "Vehicle data updated successfully"
            else:  # Insert new record
                cursor.execute(
                    """
                    INSERT INTO Vehicles (
                        Crash_Unit_ID, CRASH_RECORD_ID, CRASH_DATE, Unit_No,
                        Unit_Type, VEHICLE_ID, Make,
                        Model, Lic_Plate_State, Vehicle_Year,
                        Vehicle_Defect, Vehicle_Type, Vehicle_Use,
                        Travel_direction, maneuver, Occupant_CNT,
                        First_contact_point
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    int(self.vehicle_entries["Crash_Unit_ID"].get()) if self.vehicle_entries["Crash_Unit_ID"].get() else None,
                    self.vehicle_entries["CRASH_RECORD_ID"].get(),
                    crash_date,
                    int(self.vehicle_entries["Unit_No"].get()) if self.vehicle_entries["Unit_No"].get() else None,
                    self.vehicle_entries["Unit_Type"].get(),
                    int(self.vehicle_entries["VEHICLE_ID"].get()) if self.vehicle_entries["VEHICLE_ID"].get() else None,
                    self.vehicle_entries["Make"].get(),
                    self.vehicle_entries["Model"].get(),
                    self.vehicle_entries["Lic_Plate_State"].get(),
                    int(self.vehicle_entries["Vehicle_Year"].get()) if self.vehicle_entries["Vehicle_Year"].get() else None,
                    self.vehicle_entries["Vehicle_Defect"].get(),
                    self.vehicle_entries["Vehicle_Type"].get(),
                    self.vehicle_entries["Vehicle_Use"].get(),
                    self.vehicle_entries["Travel_direction"].get(),
                    self.vehicle_entries["maneuver"].get(),
                    int(self.vehicle_entries["Occupant_CNT"].get()) if self.vehicle_entries["Occupant_CNT"].get() else None,
                    self.vehicle_entries["First_contact_point"].get()
                )
                message = "Vehicle data saved successfully"
            
            self.conn.commit()
            messagebox.showinfo("Success", message)
            self.load_vehicles()
            self.clear_vehicle_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")
    
    def clear_vehicle_fields(self):
        """Clear all vehicle form fields"""
        self.current_vehicle_id = None
        for field, entry in self.vehicle_entries.items():
            if isinstance(entry, ttk.Combobox):
                entry.set("")
            else:
                entry.delete(0, tk.END)
    
    def delete_crash(self):
        """Delete selected accident record and related records"""
        if not self.current_crash_id:
            messagebox.showwarning("Warning", "No accident selected")
            return
        
        if not messagebox.askyesno("Confirm", "Delete this accident and all related people and vehicles?"):
            return
        
        try:
            cursor = self.conn.cursor()
            
            # First delete related people and vehicles
            cursor.execute("DELETE FROM People WHERE CRASH_RECORD_ID=?", self.current_crash_id)
            cursor.execute("DELETE FROM Vehicles WHERE CRASH_RECORD_ID=?", self.current_crash_id)
            
            # Then delete the accident
            cursor.execute("DELETE FROM Crashes WHERE CRASH_RECORD_ID=?", self.current_crash_id)
            
            self.conn.commit()
            messagebox.showinfo("Success", "Accident and related records deleted successfully")
            self.load_crashes()
            self.load_people()
            self.load_vehicles()
            self.clear_crash_fields()
            self.current_crash_id = None
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete accident: {str(e)}")
    
    def delete_person(self):
        """Delete selected person record"""
        if not self.current_person_id:
            messagebox.showwarning("Warning", "No person selected")
            return
        
        if not messagebox.askyesno("Confirm", "Delete this person record?"):
            return
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM People WHERE PERSON_ID=?", self.current_person_id)
            self.conn.commit()
            messagebox.showinfo("Success", "Person deleted successfully")
            self.load_people()
            self.clear_person_fields()
            self.current_person_id = None
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete person: {str(e)}")
    
    def delete_vehicle(self):
        """Delete selected vehicle record"""
        if not self.current_vehicle_id:
            messagebox.showwarning("Warning", "No vehicle selected")
            return
        
        if not messagebox.askyesno("Confirm", "Delete this vehicle record?"):
            return
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM Vehicles WHERE Crash_Unit_ID=?", self.current_vehicle_id)
            self.conn.commit()
            messagebox.showinfo("Success", "Vehicle deleted successfully")
            self.load_vehicles()
            self.clear_vehicle_fields()
            self.current_vehicle_id = None
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete vehicle: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TrafficCrashesSystem(root)
    root.mainloop()
