from flask import Flask, request, jsonify, render_template
import sqlite3
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Home page with HTML form
@app.route('/', methods=['GET'])
def home():
    return jsonify(message='Welcome to the Plant Nursery API')

# Home page with HTML form to add plants
@app.route('/plants/add', methods=['GET'])
def add_plant_form():
    return render_template('add_plant.html')

# POST endpoint to add a plant
@app.route('/plants', methods=['POST'])
def add_plant():
    try:
        # Retrieve data from the HTML form
        common_name = request.form['common_name']
        genus = request.form['genus']
        species = request.form['species']
        cultivar = request.form['cultivar']
        description = request.form['description']
        size = request.form['size']
        price = request.form['price']
        quantity = request.form['quantity']

        # Connect to the database
        conn = sqlite3.connect('nursery.db')
        cursor = conn.cursor()

        # Insert data into the Plants table
        cursor.execute("INSERT INTO Plants (CommonName, Genus, Species, Cultivar, Description, Size, Price, Quantity) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (common_name, genus, species, cultivar, description, size, price, quantity))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        return jsonify(message='Plant added successfully'), 200

    except Exception as e:
        return jsonify(error=str(e)), 500

from flask import request, jsonify

@app.route('/plantgroups/add', methods=['POST'])
def add_plant_group():
    try:
        # Retrieve data from the request
        group_name = request.form['group_name']
        propagation_medium = request.form['propagation_medium']
        potting_medium = request.form['potting_medium']
        testing_notes = request.form['testing_notes']
        genus = request.form['genus']
        species = request.form['species']
        cultivar = request.form['cultivar']
        quantity = request.form['quantity']
        fertilizer_name = request.form['fertilizer_name']
        application_date = request.form['application_date']
        potting_date = request.form['potting_date']
        notes = request.form['notes']

        # Connect to the database
        conn = sqlite3.connect('nursery.db')
        cursor = conn.cursor()

        # Insert data into the PlantGroups table
        cursor.execute("""
            INSERT INTO PlantGroups (GroupName, PropagationMedium, PottingMedium, TestingNotes)
            VALUES (?, ?, ?, ?)
        """, (group_name, propagation_medium, potting_medium, testing_notes))
        group_id = cursor.lastrowid

        # Insert data into the Plants table
        cursor.execute("""
            INSERT INTO Plants (CommonName, Genus, Species, Cultivar, Quantity, GroupID)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (group_name, genus, species, cultivar, quantity, group_id))
        plant_id = cursor.lastrowid

        # Insert data into the Fertilizer table
        cursor.execute("""
            INSERT INTO Fertilizer (FertilizerName, ApplicationDate, GroupID)
            VALUES (?, ?, ?)
        """, (fertilizer_name, application_date, group_id))

        # Insert data into the Potting table
        cursor.execute("""
            INSERT INTO Potting (PlantID, PottingDate, Notes)
            VALUES (?, ?, ?)
        """, (plant_id, potting_date, notes))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        return jsonify(message='Plant group added successfully'), 200

    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route('/plantgroups', methods=['GET'])
def get_plant_groups():
    try:
        # Connect to the database
        conn = sqlite3.connect('nursery.db')
        cursor = conn.cursor()

        # Retrieve data from the PlantGroups table and join with Plants, Fertilizer, and Potting tables
        cursor.execute("""
            SELECT PlantGroups.GroupID, PlantGroups.GroupName, PlantGroups.PropagationMedium,
                   PlantGroups.PottingMedium, PlantGroups.TestingNotes,
                   Plants.Genus, Plants.Species, Plants.Cultivar, Plants.Quantity,
                   Fertilizer.FertilizerName, Fertilizer.ApplicationDate,
                   Potting.PottingDate, Potting.Notes
            FROM PlantGroups
            LEFT JOIN Plants ON PlantGroups.PlantID = Plants.PlantID
            LEFT JOIN Fertilizer ON PlantGroups.FertilizerID = Fertilizer.FertilizerID
            LEFT JOIN Potting ON PlantGroups.PottingID = Potting.PottingID
        """)

        plant_groups = cursor.fetchall()

        # Close the connection
        conn.close()

        # Prepare the data in a dictionary format
        plant_group_list = []
        for group in plant_groups:
            group_dict = {
                'group_id': group[0],
                'group_name': group[1],
                'propagation_medium': group[2],
                'potting_medium': group[3],
                'testing_notes': group[4],
                'genus': group[5],
                'species': group[6],
                'cultivar': group[7],
                'quantity': group[8],
                'fertilizer_name': group[9],
                'application_date': group[10],
                'potting_date': group[11],
                'notes': group[12]
            }
            plant_group_list.append(group_dict)

        # Return the data as JSON
        return jsonify(plant_groups=plant_group_list), 200

    except Exception as e:
        return jsonify(error=str(e)), 500
        
# Home page with HTML form to add a potting record
@app.route('/potting/add', methods=['GET'])
def add_potting_record_form():
    return render_template('add_potting_record.html')

# POST endpoint to add a potting record
@app.route('/potting', methods=['POST'])
def add_potting_record():
    try:
        # Retrieve data from the request
        plant_id = request.form['plant_id']
        potting_date = request.form['potting_date']
        notes = request.form['notes']

        # Connect to the database
        conn = sqlite3.connect('nursery.db')
        cursor = conn.cursor()

        # Insert data into the Potting table
        cursor.execute("INSERT INTO Potting (PlantID, PottingDate, Notes) VALUES (?, ?, ?)",
                       (plant_id, potting_date, notes))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        return jsonify(message='Potting record added successfully'), 200

    except Exception as e:
        return jsonify(error=str(e)), 500

# Endpoint to retrieve all potting records
@app.route('/potting', methods=['GET'])
def get_potting_records():
    try:
        # Connect to the database
        conn = sqlite3.connect('nursery.db')
        cursor = conn.cursor()

        # Retrieve data from the Potting table
        cursor.execute("SELECT * FROM Potting")
        potting_records = cursor.fetchall()

        # Close the connection
        conn.close()

        # Convert the data to a list of dictionaries
        potting_record_list = []
        for record in potting_records:
            record_dict = {
                'potting_id': record[0],
                'plant_id': record[1],
                'potting_date': record[2],
                'notes': record[3]
            }
            potting_record_list.append(record_dict)

        return jsonify(potting_records=potting_record_list), 200

    except Exception as e:
        return jsonify(error=str(e)), 500
# Home page with HTML form to add a fertilizer record
@app.route('/fertilizer/add', methods=['GET'])
def add_fertilizer_record_form():
    return render_template('add_fertilizer_record.html')

# POST endpoint to add a fertilizer record
@app.route('/fertilizer', methods=['POST'])
def add_fertilizer_record():
    try:
        # Retrieve data from the request
        fertilizer_name = request.form['fertilizer_name']
        application_date = request.form['application_date']
        group_id = request.form['group_id']

        # Connect to the database
        conn = sqlite3.connect('nursery.db')
        cursor = conn.cursor()

        # Insert data into the Fertilizer table
        cursor.execute("INSERT INTO Fertilizer (FertilizerName, ApplicationDate, GroupID) VALUES (?, ?, ?)",
                       (fertilizer_name, application_date, group_id))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        return jsonify(message='Fertilizer record added successfully'), 200

    except Exception as e:
        return jsonify(error=str(e)), 500

# Endpoint to retrieve all fertilizer records
@app.route('/fertilizer', methods=['GET'])
def get_fertilizer_records():
    try:
        # Connect to the database
        conn = sqlite3.connect('nursery.db')
        cursor = conn.cursor()

        # Retrieve data from the Fertilizer table
        cursor.execute("SELECT * FROM Fertilizer")
        fertilizer_records = cursor.fetchall()

        # Close the connection
        conn.close()

        # Convert the data to a list of dictionaries
        fertilizer_record_list = []
        for record in fertilizer_records:
            record_dict = {
                'fertilizer_id': record[0],
                'fertilizer_name': record[1],
                'application_date': record[2],
                'group_id': record[3]
            }
            fertilizer_record_list.append(record_dict)

        return jsonify(fertilizer_records=fertilizer_record_list), 200

    except Exception as e:
        return jsonify(error=str(e)), 500

# Endpoint to retrieve all plants
@app.route('/plants', methods=['GET'])
def get_plants():
    try:
        # Connect to the database
        conn = sqlite3.connect('nursery.db')
        cursor = conn.cursor()

        # Retrieve data from the Plants table
        cursor.execute("SELECT * FROM Plants")
        plants = cursor.fetchall()

        # Close the connection
        conn.close()

        # Convert the data to a list of dictionaries
        plant_list = []
        for plant in plants:
            plant_dict = {
                'common_name': plant[1],
                'genus': plant[2],
                'species': plant[3],
                'cultivar': plant[4],
                'description': plant[5],
                'size': plant[6],
                'price': plant[7],
                'quantity': plant[8]
            }
            plant_list.append(plant_dict)

        return jsonify(plants=plant_list), 200

    except Exception as e:
        return jsonify(error=str(e)), 500

# Endpoint to search plants by the provided parameters
@app.route('/plants/search', methods=['GET'])
def search_plants():
    try:
        # Retrieve query parameters from the request
        genus = request.args.get('genus')
        species = request.args.get('species')
        cultivar = request.args.get('cultivar')

        # Connect to the database
        conn = sqlite3.connect('nursery.db')
        cursor = conn.cursor()

        # Construct the SQL query based on the provided parameters
        query = "SELECT * FROM Plants WHERE 1=1"
        params = []

        if genus:
            query += " AND Genus = ?"
            params.append(genus)

        if species:
            query += " AND Species = ?"
            params.append(species)

        if cultivar:
            query += " AND Cultivar = ?"
            params.append(cultivar)

        # Execute the query
        cursor.execute(query, tuple(params))
        plants = cursor.fetchall()

        # Close the connection
        conn.close()

        # Convert the data to a list of dictionaries
        plant_list = []
        for plant in plants:
            plant_dict = {
                'common_name': plant[1],
                'genus': plant[2],
                'species': plant[3],
                'cultivar': plant[4],
                'description': plant[5],
                'size': plant[6],
                'price': plant[7],
                'quantity': plant[8]
            }
            plant_list.append(plant_dict)

        return jsonify(plants=plant_list), 200

    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)