from flask import Flask, render_template, request, jsonify, redirect, url_for
import psycopg2
import os

app = Flask(__name__)

db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'dbname': os.getenv('DB_NAME', 'postgres'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', ''),
    'port': os.getenv('DB_PORT', '5432')
}
# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to save data to the database
@app.route('/send_to_db', methods=['POST'])
def send_to_db():
    data = request.json.get('data')
    
    try:
        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Insert data into the database (Assuming a table named 'data_table' with a column 'data')
        for item in data:
            cursor.execute("INSERT INTO data_table (item, units, price, date) VALUES (%s, %s, %s, %s)", (item['item'], item['units'], item['price'], item['date']))
        conn.commit()
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/new_item')
def new_item():
    return render_template('new_item.html')

# Route to save a new item in the item table
@app.route('/save_item', methods=['POST'])
def save_item():
    item_name = request.form['item_name']
    if item_name:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO item (item_name) VALUES (%s)", (item_name,))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
