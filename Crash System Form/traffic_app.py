import streamlit as st
import pyodbc
from datetime import datetime

# Database connection function
def get_db_connection():
    server = 'DESKTOP-N4J2UNJ'
    database = 'Traffic_Crashes'
    driver = '{ODBC Driver 17 for SQL Server}'
    conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    return pyodbc.connect(conn_str)

# Insert crash data
def insert_crash(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Crashes (
                CRASH_RECORD_ID, POSTED_SPEED_LIMIT, TRAFFIC_CONTROL_DEVICE,
                DEVICE_CONDITION, WEATHER_CONDITION, LIGHTING_CONDITION,
                FIRST_CRASH_TYPE, TRAFFICWAY_TYPE, ALIGNMENT,
                ROADWAY_SURFACE_COND, ROAD_DEFECT, CRASH_TYPE,
                DAMAGE, PRIM_CONTRIBUTORY_CAUSE, SEC_CONTRIBUTORY_CAUSE,
                NUM_UNITS, MOST_SEVERE_INJURY, INJURIES_TOTAL,
                INJURIES_FATAL, LATITUDE, LONGITUDE
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, tuple(data.values()))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Database error: {e}")
        return False
    finally:
        conn.close()

# Insert vehicle data (with manual VEHICLE_ID)
def insert_vehicle(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Vehicles (
                VEHICLE_ID, CRASH_RECORD_ID, Unit_No, Unit_Type, 
                Make, Model, Lic_Plate_State, Vehicle_Year, Vehicle_Defect, 
                Vehicle_Type, Vehicle_Use, Travel_direction, maneuver, 
                Occupant_CNT, First_contact_point
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data['VEHICLE_ID'], data['CRASH_RECORD_ID'],
                data['Unit_No'], data['Unit_Type'], data['Make'], data['Model'],
                data['Lic_Plate_State'], data['Vehicle_Year'], data['Vehicle_Defect'],
                data['Vehicle_Type'], data['Vehicle_Use'], data['Travel_direction'],
                data['maneuver'], data['Occupant_CNT'], data['First_contact_point']
            ))
        conn.commit()
        return data['VEHICLE_ID']  # Return the vehicle ID
    except Exception as e:
        st.error(f"Database error: {e}")
        return None
    finally:
        conn.close()

# Insert person data (with VEHICLE_ID from session state)
def insert_person(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Get VEHICLE_ID from session state
        vehicle_id = st.session_state.get('current_vehicle_id')
        if not vehicle_id:
            st.error("No vehicle selected! Please add a vehicle first.")
            return False
            
        cursor.execute("""
            INSERT INTO People (
                VEHICLE_ID, CRASH_RECORD_ID, PERSON_TYPE, SEX, AGE, 
                DRIVERS_LICENSE_STATE, DRIVERS_LICENSE_CLASS, SAFETY_EQUIPMENT, 
                AIRBAG_DEPLOYED, EJECTION, INJURY_CLASSIFICATION, DRIVER_ACTION, 
                PHYSICAL_CONDITION, BAC_RESULT
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                vehicle_id, data['CRASH_RECORD_ID'], data['PERSON_TYPE'],
                data['SEX'], data['AGE'], data['DRIVERS_LICENSE_STATE'],
                data['DRIVERS_LICENSE_CLASS'], data['SAFETY_EQUIPMENT'],
                data['AIRBAG_DEPLOYED'], data['EJECTION'], data['INJURY_CLASSIFICATION'],
                data['DRIVER_ACTION'], data['PHYSICAL_CONDITION'], data['BAC_RESULT']
            ))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Database error: {e}")
        return False
    finally:
        conn.close()

# Get vehicles for a specific crash
def get_vehicles(crash_record_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT VEHICLE_ID, Make, Model, Unit_No 
            FROM Vehicles 
            WHERE CRASH_RECORD_ID = ?
            """, (crash_record_id,))
        return cursor.fetchall()
    except Exception as e:
        st.error(f"Database error: {e}")
        return []
    finally:
        conn.close()

# Crash form
def crash_form():
    st.header("Crash Information")
    with st.form("crash_form"):
        crash_record_id = st.text_input("Crash Record ID*", max_chars=50)
        
        cols = st.columns(2)
        
        with cols[0]:
            posted_speed_limit = st.number_input("Posted Speed Limit", min_value=0, max_value=100)
            traffic_control_device = st.text_input("Traffic Control Device", max_chars=100)
            device_condition = st.text_input("Device Condition", max_chars=100)
            weather_condition = st.text_input("Weather Condition", max_chars=100)
            lighting_condition = st.text_input("Lighting Condition", max_chars=100)
            first_crash_type = st.text_input("First Crash Type", max_chars=100)
            trafficway_type = st.text_input("Trafficway Type", max_chars=100)
            alignment = st.text_input("Alignment", max_chars=100)
        
        with cols[1]:
            roadway_surface_cond = st.text_input("Roadway Surface Condition", max_chars=100)
            road_defect = st.text_input("Road Defect", max_chars=100)
            crash_type = st.text_input("Crash Type", max_chars=100)
            damage = st.selectbox("Damage", ["OVER $1,500", "$501 - $1,500", "$500 OR LESS"])
            prim_contributory_cause = st.text_input("Primary Contributory Cause", max_chars=100)
            sec_contributory_cause = st.text_input("Secondary Contributory Cause", max_chars=100)
            num_units = st.number_input("Number of Units", min_value=1, max_value=20)
            most_severe_injury = st.text_input("Most Severe Injury", max_chars=100)
            injuries_total = st.number_input("Total Injuries", min_value=0)
            injuries_fatal = st.number_input("Fatal Injuries", min_value=0)
            latitude = st.number_input("Latitude", format="%.6f")
            longitude = st.number_input("Longitude", format="%.6f")
        
        submitted = st.form_submit_button("Submit Crash Data")
        if submitted:
            if not crash_record_id:
                st.error("Crash Record ID is required!")
            else:
                crash_data = {
                    'CRASH_RECORD_ID': crash_record_id,
                    'POSTED_SPEED_LIMIT': posted_speed_limit,
                    'TRAFFIC_CONTROL_DEVICE': traffic_control_device,
                    'DEVICE_CONDITION': device_condition,
                    'WEATHER_CONDITION': weather_condition,
                    'LIGHTING_CONDITION': lighting_condition,
                    'FIRST_CRASH_TYPE': first_crash_type,
                    'TRAFFICWAY_TYPE': trafficway_type,
                    'ALIGNMENT': alignment,
                    'ROADWAY_SURFACE_COND': roadway_surface_cond,
                    'ROAD_DEFECT': road_defect,
                    'CRASH_TYPE': crash_type,
                    'DAMAGE': damage,
                    'PRIM_CONTRIBUTORY_CAUSE': prim_contributory_cause,
                    'SEC_CONTRIBUTORY_CAUSE': sec_contributory_cause,
                    'NUM_UNITS': num_units,
                    'MOST_SEVERE_INJURY': most_severe_injury,
                    'INJURIES_TOTAL': injuries_total,
                    'INJURIES_FATAL': injuries_fatal,
                    'LATITUDE': latitude,
                    'LONGITUDE': longitude
                }
                if insert_crash(crash_data):
                    st.session_state['current_crash_id'] = crash_record_id
                    st.success("Crash data saved successfully!")
                    return crash_record_id
    return None

# Vehicle form (with manual VEHICLE_ID entry)
def vehicle_form(crash_record_id):
    st.header("Vehicle Information")
    
    with st.form("vehicle_form"):
        st.write(f"Crash Record ID: {crash_record_id}")
        
        # Manual VEHICLE_ID entry
        vehicle_id = st.text_input("Vehicle ID*", max_chars=50, 
                                 help="Enter your custom vehicle identifier")
        
        cols = st.columns(2)
        
        with cols[0]:
            unit_no = st.text_input("Unit Number*", max_chars=10)
            unit_type = st.text_input("Unit Type", max_chars=50)
            make = st.text_input("Make*", max_chars=50)
            model = st.text_input("Model*", max_chars=50)
            lic_plate_state = st.text_input("License Plate State", max_chars=2)
            vehicle_year = st.number_input("Vehicle Year*", min_value=1900, max_value=datetime.now().year)
        
        with cols[1]:
            vehicle_defect = st.text_input("Vehicle Defect", max_chars=100)
            vehicle_type = st.text_input("Vehicle Type", max_chars=50)
            vehicle_use = st.text_input("Vehicle Use", max_chars=50)
            travel_direction = st.text_input("Travel Direction", max_chars=50)
            maneuver = st.text_input("Maneuver", max_chars=50)
            occupant_cnt = st.number_input("Occupant Count", min_value=0, max_value=50)
            first_contact_point = st.text_input("First Contact Point", max_chars=50)
        
        submitted = st.form_submit_button("Submit Vehicle Data")
        if submitted:
            if not vehicle_id or not unit_no or not make or not model or not vehicle_year:
                st.error("Fields marked with * are required!")
            else:
                vehicle_data = {
                    'VEHICLE_ID': vehicle_id,
                    'CRASH_RECORD_ID': crash_record_id,
                    'Unit_No': unit_no,
                    'Unit_Type': unit_type,
                    'Make': make,
                    'Model': model,
                    'Lic_Plate_State': lic_plate_state,
                    'Vehicle_Year': vehicle_year,
                    'Vehicle_Defect': vehicle_defect,
                    'Vehicle_Type': vehicle_type,
                    'Vehicle_Use': vehicle_use,
                    'Travel_direction': travel_direction,
                    'maneuver': maneuver,
                    'Occupant_CNT': occupant_cnt,
                    'First_contact_point': first_contact_point
                }
                if insert_vehicle(vehicle_data):
                    # Store the vehicle ID in session state
                    st.session_state['current_vehicle_id'] = vehicle_id
                    st.success("Vehicle data saved successfully!")
                    st.session_state['show_person_form'] = True  # Flag to show person form next

# Person form (uses the manually entered VEHICLE_ID)
def person_form(crash_record_id):
    if 'current_vehicle_id' not in st.session_state:
        st.warning("Please add a vehicle first before adding people.")
        return
    
    st.header("Person Information")
    st.write(f"Vehicle ID: {st.session_state['current_vehicle_id']}")
    st.write(f"Crash Record ID: {crash_record_id}")
    
    with st.form("person_form"):
        cols = st.columns(2)
        
        with cols[0]:
            person_type = st.text_input("Person Type*", max_chars=50)
            sex = st.selectbox("Sex*", ["", "Male", "Female", "Other"])
            age = st.number_input("Age*", min_value=0, max_value=120)
            drivers_license_state = st.text_input("Driver's License State", max_chars=2)
            drivers_license_class = st.text_input("Driver's License Class", max_chars=10)
            safety_equipment = st.text_input("Safety Equipment", max_chars=100)
        
        with cols[1]:
            airbag_deployed = st.selectbox("Airbag Deployed", ["", "Yes", "No", "Unknown"])
            ejection = st.selectbox("Ejection", ["", "Yes", "No", "Partial"])
            injury_classification = st.text_input("Injury Classification", max_chars=50)
            driver_action = st.text_input("Driver Action", max_chars=100)
            physical_condition = st.text_input("Physical Condition", max_chars=100)
            bac_result = st.number_input("BAC Result", min_value=0.0, max_value=1.0, step=0.01, format="%.2f")
        
        submitted = st.form_submit_button("Submit Person Data")
        if submitted:
            if not person_type or not sex or not age:
                st.error("Fields marked with * are required!")
            else:
                person_data = {
                    'CRASH_RECORD_ID': crash_record_id,
                    'PERSON_TYPE': person_type,
                    'SEX': sex,
                    'AGE': age,
                    'DRIVERS_LICENSE_STATE': drivers_license_state,
                    'DRIVERS_LICENSE_CLASS': drivers_license_class,
                    'SAFETY_EQUIPMENT': safety_equipment,
                    'AIRBAG_DEPLOYED': airbag_deployed,
                    'EJECTION': ejection,
                    'INJURY_CLASSIFICATION': injury_classification,
                    'DRIVER_ACTION': driver_action,
                    'PHYSICAL_CONDITION': physical_condition,
                    'BAC_RESULT': bac_result
                }
                if insert_person(person_data):
                    st.success("Person data saved successfully!")

# Main app with sequential workflow
def main():
    st.set_page_config(page_title="Traffic Crashes Data Entry", layout="wide")
    st.title("Traffic Crashes Data Entry System")
    
    # Sequential workflow
    if 'current_crash_id' not in st.session_state:
        st.header("1. Enter Crash Data")
        crash_record_id = crash_form()
        if crash_record_id:
            st.session_state['current_crash_id'] = crash_record_id
            st.experimental_rerun()
    else:
        crash_record_id = st.session_state['current_crash_id']
        
        if 'show_person_form' not in st.session_state:
            st.header("2. Enter Vehicle Data")
            vehicle_form(crash_record_id)
        else:
            st.header("3. Enter Person Data")
            person_form(crash_record_id)
            
            if st.button("Add Another Person"):
                st.experimental_rerun()
            
            if st.button("Add Another Vehicle"):
                del st.session_state['show_person_form']
                st.experimental_rerun()

if __name__ == "__main__":
    main()