from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Enable CORS
CORS(app)

# -----------------------------------
# DATABASE CONFIG
# -----------------------------------
db_config = {
    "host": "database-2.chue8qoo452n.eu-north-1.rds.amazonaws.com",
    "user": "admin",
    "password": "Apandey1357"
}

DATABASE_NAME = "database-2"

# -----------------------------------
# CREATE DATABASE IF NOT EXISTS
# -----------------------------------
def create_database():

    try:
        connection = mysql.connector.connect(**db_config)

        cursor = connection.cursor()

        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DATABASE_NAME}`")

        print("Database created or already exists")

        cursor.close()
        connection.close()

    except Error as e:
        print("Database creation error:", e)

# -----------------------------------
# GET DB CONNECTION
# -----------------------------------
def get_db_connection():

    try:
        connection = mysql.connector.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"],
            database=DATABASE_NAME
        )

        return connection

    except Error as e:
        print("Database connection error:", e)
        return None

# -----------------------------------
# CREATE TABLE
# -----------------------------------
def create_table():

    connection = get_db_connection()

    if connection:

        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100)
            )
        """)

        connection.commit()

        cursor.close()
        connection.close()

        print("Users table ready")

# -----------------------------------
# HOME ROUTE
# -----------------------------------
@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "Flask + RDS API is running successfully!"
    })

# -----------------------------------
# GET USERS
# -----------------------------------
@app.route("/users", methods=["GET"])
def get_users():

    connection = get_db_connection()

    if not connection:
        return jsonify({
            "error": "Database connection failed"
        }), 500

    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users")

    users = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(users)

# -----------------------------------
# ADD USER
# -----------------------------------
@app.route("/users", methods=["POST"])
def add_user():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({
            "error": "Name and Email are required"
        }), 400

    connection = get_db_connection()

    if not connection:
        return jsonify({
            "error": "Database connection failed"
        }), 500

    cursor = connection.cursor()

    query = """
        INSERT INTO users (name, email)
        VALUES (%s, %s)
    """

    values = (name, email)

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "message": "User added successfully"
    })

# -----------------------------------
# START APP
# -----------------------------------
if __name__ == "__main__":

    create_database()

    create_table()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
