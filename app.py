from flask import Flask, render_template, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Database configuration
# db_config = {
#     'host': 'localhost',
#     'dbname': 'postgres',
#     'user': 'postgres',
#     'password': 'hjkl',
#     'port': '5432'
# }
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


if __name__ == '__main__':
    app.run(debug=True)
