# 🚀 AWS 3-Tier Architecture Project

# 📌 Project Overview

This project demonstrates a complete production-style AWS 3-tier architecture deployment using:

* Amazon S3
* CloudFront CDN
* EC2 Ubuntu Server
* Flask REST API
* Amazon RDS MySQL
* IAM Roles & Policies
* CloudWatch Monitoring
* Git & GitHub

The project allows users to submit their name and email through a frontend application, store the data in an RDS MySQL database, and dynamically fetch/display users using a Flask backend API.

---

# 🏗️ Architecture Diagram

```text
Users
   ↓
CloudFront CDN
   ↓
S3 Static Website
   ↓
EC2 Flask Backend API
   ↓
RDS MySQL Database
```

---

# 📌 AWS Services Used

| Service         | Purpose               |
| --------------- | --------------------- |
| S3              | Frontend hosting      |
| CloudFront      | CDN + HTTPS delivery  |
| EC2             | Flask backend hosting |
| RDS MySQL       | Database              |
| IAM             | Secure permissions    |
| CloudWatch      | Monitoring & alarms   |
| Security Groups | Firewall rules        |
| GitHub          | Version control       |

---

# 📂 Project Structure

```text
aws-3tier-project/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── backend/
│   ├── app.py
│   └── requirements.txt
│
├── screenshots/
│
└── README.md
```

---

# 🎯 Project Workflow

```text
User opens frontend website
        ↓
Frontend sends API request to Flask backend
        ↓
Flask API processes request
        ↓
Flask inserts/fetches data from RDS MySQL
        ↓
Frontend dynamically updates user list
```

---

# 🔥 STEP 1 — Launch EC2 Instance

## EC2 Configuration

| Setting        | Value                |
| -------------- | -------------------- |
| AMI            | Ubuntu               |
| Instance Type  | t2.micro             |
| Storage        | 8 GB                 |
| Key Pair       | Created new key pair |
| Security Group | Custom SG            |

---

# 🔐 EC2 Security Group Rules

## Inbound Rules

| Type       | Port | Source   |
| ---------- | ---- | -------- |
| SSH        | 22   | My IP    |
| Custom TCP | 5000 | Anywhere |

---

# 🔥 STEP 2 — Connect EC2 Using SSH

```bash
ssh -i your-key.pem ubuntu@YOUR-EC2-PUBLIC-IP
```

---

# ❌ ISSUE FACED — SSH Connection Failed

## Error

```text
ssh: connect to host xx.xx.xx.xx port 22: Software caused connection abort
```

## Root Cause

SSH port 22 was not allowed in Security Group.

## Fix

Added inbound SSH rule.

---

# 🔥 STEP 3 — Update Ubuntu Server

```bash
sudo apt update
sudo apt upgrade -y
```

---

# 🔥 STEP 4 — Install Python & Pip

```bash
sudo apt install python3 python3-pip python3-venv -y
```

---

# 🔥 STEP 5 — Create Flask Project

```bash
mkdir flask-app
cd flask-app
```

---

# 🔥 STEP 6 — Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# 🔥 STEP 7 — Install Required Packages

```bash
pip install flask flask-cors mysql-connector-python
```

---

# 🔥 STEP 8 — Create Flask Backend

```bash
nano app.py
```

---

# ❌ ISSUE FACED — Typed Python Code in Terminal

## Error

```text
db_config = {...}
Command 'db_config' not found
```

## Root Cause

Python code typed directly into Linux terminal.

## Fix

Opened app.py and pasted code inside file.

---

# 🔥 STEP 9 — Run Flask App

```bash
python3 app.py
```

---

# 🎉 Flask API Output

```json
{
  "message": "Flask API is running!"
}
```

---

# 🔥 STEP 10 — Create Amazon RDS MySQL Database

## RDS Configuration

| Setting       | Value      |
| ------------- | ---------- |
| Engine        | MySQL      |
| Template      | Free Tier  |
| Public Access | Yes        |
| DB Identifier | database-2 |
| Username      | admin      |

---

# ❌ ISSUE FACED — Security Group Not Showing

## Root Cause

RDS and EC2 were not properly aligned in same VPC.

## Fix

Created fresh RDS inside same VPC.

---

# 🔥 STEP 11 — Configure RDS Security Group

| Type         | Port | Source             |
| ------------ | ---- | ------------------ |
| MySQL/Aurora | 3306 | EC2 Security Group |

---

# ❌ ISSUE FACED — Database Connection Timeout

## Error

```text
Can't connect to MySQL server on port 3306
```

## Root Cause

MySQL inbound rule missing.

## Fix

Allowed port 3306 from EC2 SG.

---

# 🔥 STEP 12 — Install MySQL Client

```bash
sudo apt install mysql-client -y
```

---

# ❌ ISSUE FACED — SSL Error

## Error

```text
TLS/SSL error: self-signed certificate
```

## Fix

Used:

```python
"ssl_disabled": True
```

inside Flask database config.

---

# 🔥 STEP 13 — Create Database

```sql
CREATE DATABASE flaskdb;
SHOW DATABASES;
```

---

# ❌ ISSUE FACED — Unknown Database

## Error

```text
Unknown database 'database-2'
```

## Root Cause

`database-2` was RDS instance name, not actual database name.

## Fix

Created real MySQL database:

```sql
CREATE DATABASE flaskdb;
```

---

# 🔥 STEP 14 — Final Backend app.py

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Database configuration

db_config = {
    "host": "RDS-ENDPOINT",
    "user": "admin",
    "password": "YOUR_PASSWORD",
    "database": "flaskdb",
    "ssl_disabled": True
}

# Database connection function

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Create table

def create_table():
    connection = get_db_connection()
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

@app.route('/')
def home():
    return jsonify({"message": "Flask + RDS API is running successfully!"})

@app.route('/users', methods=['GET'])
def get_users():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users")

    users = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(users)

@app.route('/users', methods=['POST'])
def add_user():

    data = request.get_json()

    name = data['name']
    email = data['email']

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO users (name, email) VALUES (%s, %s)",
        (name, email)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({"message": "User added successfully"})

if __name__ == '__main__':
    create_table()
    app.run(host='0.0.0.0', port=5000)
```

---

# 🔍 Backend Code Explanation

## Flask

```python
from flask import Flask
```

Used to create REST API server.

---

# WHY FLASK?

Benefits:

✅ lightweight
✅ beginner friendly
✅ API focused

---

## request

Used to receive frontend data.

---

## jsonify

Converts Python dictionary into JSON response.

---

## CORS

```python
from flask_cors import CORS
```

Allows frontend and backend communication.

---

# WHY CORS?

Frontend:

```text
CloudFront/S3
```

Backend:

```text
EC2 IP
```

Different origins.

Without CORS:

❌ browser blocks requests.

---

## mysql.connector

Connects Python with MySQL database.

---

## app = Flask(**name**)

Creates Flask application.

---

## Database Config

Stores:

* RDS endpoint
* username
* password
* database name

---

## ssl_disabled

Used because MySQL SSL mismatch issue occurred.

---

## get_db_connection()

Reusable database connection function.

---

## create_table()

Automatically creates table if not exists.

---

## SQL Query

```sql
CREATE TABLE IF NOT EXISTS users
```

Creates users table.

---

## PRIMARY KEY

```sql
id INT AUTO_INCREMENT PRIMARY KEY
```

Automatically creates unique ID.

---

## @app.route

Defines API endpoints.

---

## GET Method

Used for fetching data.

---

## POST Method

Used for sending data.

---

## request.get_json()

Reads frontend JSON data.

---

## SQL INSERT

```sql
INSERT INTO users
```

Stores data into RDS database.

---

## connection.commit()

Saves data permanently.

Without commit:

❌ data not saved.

---

## connection.close()

Closes database connection.

---

# WHY CLOSE CONNECTIONS?

Avoids:

❌ memory leaks
❌ too many DB connections

---

## app.run()

Starts Flask server.

---

## host='0.0.0.0'

Allows public access.

Without this:

❌ accessible only inside EC2.

---

# 🔥 STEP 15 — Frontend Development

## Frontend Files

```text
index.html
style.css
script.js
```

---

# 📄 index.html

```html
<!DOCTYPE html>
<html>
<head>
    <title>AWS 3-Tier Architecture Project</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

<h1>AWS 3-Tier Architecture Project</h1>

<input type="text" id="name" placeholder="Enter Name">
<input type="email" id="email" placeholder="Enter Email">

<button onclick="addUser()">Add User</button>

<h2>Users List</h2>

<ul id="users"></ul>

<script src="script.js"></script>

</body>
</html>
```

---

# 🔍 Frontend Code Explanation

## Input Fields

Used to take user input.

---

## id="name"

Allows JavaScript to access input field.

---

## Button

```html
<button onclick="addUser()">
```

Runs JavaScript function.

---

## Users List

```html
<ul id="users"></ul>
```

Dynamic container where user data appears.

---

# 🎨 style.css

```css
body {
    font-family: Arial;
    margin: 40px;
}

input {
    padding: 10px;
    margin: 5px;
}

button {
    padding: 10px 20px;
}
```

---

# 🔍 CSS Explanation

## font-family

Changes webpage font.

---

## margin

Adds outer spacing.

---

## padding

Adds inner spacing.

---

# ⚙️ script.js

```javascript
const API_URL = "http://EC2-PUBLIC-IP:5000";

async function getUsers() {

    const response = await fetch(`${API_URL}/users`);

    const users = await response.json();

    const usersList = document.getElementById("users");

    usersList.innerHTML = "";

    users.forEach(user => {

        const li = document.createElement("li");

        li.textContent = `${user.name} - ${user.email}`;

        usersList.appendChild(li);
    });
}

async function addUser() {

    const name = document.getElementById("name").value;

    const email = document.getElementById("email").value;

    await fetch(`${API_URL}/users`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ name, email })
    });

    getUsers();
}

getUsers();
```

---

# 🔍 JavaScript Explanation

## API_URL

Stores Flask backend URL.

---

## async function

Allows waiting for API response.

---

## fetch()

Makes HTTP request.

Flow:

```text
Frontend → Flask API
```

---

## response.json()

Converts API response into JavaScript object.

---

## JSON.stringify()

Converts JavaScript object into JSON format.

---

# WHY JSON?

Industry-standard API format.

---

# 🔄 COMPLETE DATA FLOW

```text
User enters form
      ↓
JavaScript sends POST request
      ↓
Flask API receives request
      ↓
Flask inserts data into RDS
      ↓
Flask returns JSON response
      ↓
Frontend updates user list
```

---

# 🔥 STEP 16 — Upload Frontend to S3

## S3 Configuration

| Setting                | Value   |
| ---------------------- | ------- |
| Static Website Hosting | Enabled |
| Public Access          | Enabled |

Uploaded:

* index.html
* style.css
* script.js

---

# 🔥 STEP 17 — Bucket Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicRead",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::YOUR-BUCKET/*"
    }
  ]
}
```

---

# 🔥 STEP 18 — Configure CloudFront

## CloudFront Settings

| Setting             | Value                  |
| ------------------- | ---------------------- |
| Origin              | S3 Bucket              |
| Viewer Protocol     | Redirect HTTP to HTTPS |
| Default Root Object | index.html             |

---

# ❌ ISSUE FACED — Access Denied

## Root Cause

index.html not configured.

## Fix

Added:

```text
index.html
```

as default root object.

---

# 🔥 STEP 19 — CloudWatch Monitoring

Configured:

* CPU monitoring
* EC2 metrics
* alarms

---

# 🔥 STEP 20 — IAM Role & Policies

Created IAM Role:

```text
EC2-CloudWatch-Role
```

Attached policies:

* CloudWatchAgentServerPolicy
* Custom-S3-Read-Policy

---

# 🔥 STEP 21 — GitHub Setup

```bash
git init
git add .
git commit -m "Initial commit"
```

---

# ❌ ISSUE FACED — GitHub Authentication Failed

## Error

```text
Invalid username or token
```

## Root Cause

GitHub no longer supports password authentication.

## Fix

Used GitHub Personal Access Token (PAT).

---

# ☁️ AWS SERVICES EXPLANATION

# Amazon S3

Used for frontend hosting.

Benefits:

✅ cheap
✅ scalable
✅ highly available

---

# CloudFront

AWS CDN service.

Benefits:

✅ HTTPS
✅ caching
✅ faster loading

---

# Amazon EC2

Virtual Linux server.

Runs Flask backend.

---

# Amazon RDS

Managed MySQL database service.

Benefits:

✅ backups
✅ maintenance
✅ scalability

---

# Security Groups

Acts like firewall.

| Port | Purpose   |
| ---- | --------- |
| 22   | SSH       |
| 5000 | Flask API |
| 3306 | MySQL     |

---

# IAM Role

Provides secure AWS permissions.

Avoids hardcoded credentials.

---

# CloudWatch

Used for:

* monitoring
* metrics
* alarms

---

# 🚀 Future Improvements

* Application Load Balancer (ALB)
* Auto Scaling Group
* Bastion Host
* Multi-AZ RDS
* Private Subnets
* NAT Gateway
* Docker
* Terraform
* CI/CD Pipeline
* Kubernetes

---

# 🧠 Interview Questions Covered

* What is 3-tier architecture?
* Why use CloudFront?
* Why use RDS?
* What are Security Groups?
* Why IAM Roles?
* How frontend communicates with backend?
* What issues did you face?
* How did you troubleshoot AWS networking?

---

# 🏆 Final Skills Learned

## AWS Skills

* EC2
* RDS
* S3
* CloudFront
* IAM
* CloudWatch
* Networking

---

## DevOps Skills

* Git
* GitHub
* Linux
* Flask deployment
* REST APIs
* Debugging
* Security Groups

---

# 👨‍💻 Author

## Avinash Pandey

AWS | DevOps | Cloud Computing | Python Flask

---

# ⭐ Final Result

Successfully built and deployed a complete AWS 3-tier architecture project using frontend hosting, backend APIs, RDS database, monitoring, IAM security, GitHub integration, and real-world cloud troubleshooting.
