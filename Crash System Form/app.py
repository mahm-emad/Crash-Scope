from flask import Flask, render_template, request, redirect, url_for, flash
from db_helper import Database

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for flash messages
db = Database()

# Home page with links to both forms
@app.route('/')
def home():
    return render_template('home.html')

# Vehicles form routes
@app.route('/vehicles', methods=['GET', 'POST'])
def vehicles():
    if request.method == 'POST':
        # Get form data
        vehicle_data = {
            'Unit_No': request.form.get('unit_no'),
            'Unit_Type': request.form.get('unit_type'),
            'Make': request.form.get('make'),
            'Model': request.form.get('model'),
            'Lic_Plate_State': request.form.get('lic_plate_state'),
            'Vehicle_Year': request.form.get('vehicle_year'),
            'Vehicle_Defect': request.form.get('vehicle_defect'),
            'Vehicle_Type': request.form.get('vehicle_type'),
            'Vehicle_Use': request.form.get('vehicle_use'),
            'Travel_direction': request.form.get('travel_direction'),
            'maneuver': request.form.get('maneuver'),
            'Occupant_CNT': request.form.get('occupant_cnt'),
            'First_contact_point': request.form.get('first_contact_point')
        }

        # Insert into database
        query = """
        INSERT INTO Vehicles (
            Unit_No, Unit_Type, Make, Model, 
            Lic_Plate_State, Vehicle_Year, Vehicle_Defect, Vehicle_Type, 
            Vehicle_Use, Travel_direction, maneuver, Occupant_CNT, 
            First_contact_point
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        if db.execute_query(query, tuple(vehicle_data.values())):
            flash('Vehicle data saved successfully!', 'success')
        else:
            flash('Error saving vehicle data!', 'error')
        
        return redirect(url_for('vehicles'))
    
    return render_template('vehicles_form.html')

# People form routes
@app.route('/people', methods=['GET', 'POST'])
def people():
    if request.method == 'POST':
        # Get form data
        person_data = {
            'PERSON_TYPE': request.form.get('person_type'),
            'SEX': request.form.get('sex'),
            'AGE': request.form.get('age'),
            'DRIVERS_LICENSE_STATE': request.form.get('drivers_license_state'),
            'DRIVERS_LICENSE_CLASS': request.form.get('drivers_license_class'),
            'SAFETY_EQUIPMENT': request.form.get('safety_equipment'),
            'AIRBAG_DEPLOYED': request.form.get('airbag_deployed'),
            'EJECTION': request.form.get('ejection'),
            'INJURY_CLASSIFICATION': request.form.get('injury_classification'),
            'DRIVER_ACTION': request.form.get('driver_action'),
            'PHYSICAL_CONDITION': request.form.get('physical_condition'),
            'BAC_RESULT': request.form.get('bac_result')
        }

        # Insert into database
        query = """
        INSERT INTO People (
            PERSON_TYPE, SEX, AGE, DRIVERS_LICENSE_STATE, 
            DRIVERS_LICENSE_CLASS, SAFETY_EQUIPMENT, AIRBAG_DEPLOYED, 
            EJECTION, INJURY_CLASSIFICATION, DRIVER_ACTION, 
            PHYSICAL_CONDITION, BAC_RESULT
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        if db.execute_query(query, tuple(person_data.values())):
            flash('Person data saved successfully!', 'success')
        else:
            flash('Error saving person data!', 'error')
        
        return redirect(url_for('people'))
    
    return render_template('people_form.html')

if __name__ == '__main__':
    app.run(debug=True)