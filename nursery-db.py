from flask import Flask, request, render_template, jsonify
import sqlite3

app = Flask(__name__)

# Home page with HTML form
@app.route('/', methods=['GET'])
def home():
    return render_template('plants.html')

@app.route('/plants/add', methods=['GET', 'POST'])
def add_plant_form():
    if request.method == 'GET':
        return render_template('add_plant.html')
    elif request.method == 'POST':
        try:
            # Retrieve data from the HTML form
            common_name = request.form['common_name']
            genus = request.form['genus']
            species = request.form['species']
            cultivar = request.form['cultivar']
            description = request.form['description']
            size = request.form['size']
            price = request.form['price']
            group = request.form['group']
            quantity = request.form['quantity']
            potting_medium = request.form['potting_medium']
            potting_date = request.form['potting_date']
            fertilizer_name = request.form['fertilizer_name']
            application_date = request.form['application_date']
            notes = request.form['notes']

            # Connect to the database
            conn = sqlite3.connect('nursery.db')
            cursor = conn.cursor()

            # Insert data into the Plants table
            cursor.execute("""
                INSERT INTO Plants (
                    CommonName, Genus, Species, Cultivar, Description, Size, Price, GroupName, Quantity,
                    PottingMedium, PottingDate,FertilizerName, ApplicationDate, Notes
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                common_name, genus, species, cultivar, description, size, price, group, quantity,
                potting_medium, potting_date, fertilizer_name, application_date, notes
            ))

            # Commit the changes and close the connection
            conn.commit()
            conn.close()

            return jsonify(message='Plant added successfully'), 200

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

        return render_template('plants.html', plants=plants)

    except Exception as e:
        return jsonify(error=str(e))

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

        return render_template('plants.html', plants=plants)

    except Exception as e:
        return jsonify(error=str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
