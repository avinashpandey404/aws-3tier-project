# 🚀 AWS 3-Tier Architecture Project

## 📌 Project Overview

This project demonstrates a complete production-style AWS 3-tier architecture deployment using:

- Amazon S3
- CloudFront CDN
- EC2 Ubuntu Server
- Flask REST API
- Amazon RDS MySQL
- IAM Roles & Policies
- CloudWatch Monitoring
- Git & GitHub

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

| Service | Purpose |
|---|---|
| S3 | Frontend hosting |
| CloudFront | CDN + HTTPS delivery |
| EC2 | Flask backend hosting |
| RDS MySQL | Database |
| IAM | Secure permissions |
| CloudWatch | Monitoring & alarms |
| Security Groups | Firewall rules |
| GitHub | Version control |

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

| Setting | Value |
|---|---|
| AMI | Ubuntu |
| Instance Type | t3.micro / t2.micro |
| Storage | 8 GB |
| Key Pair | Created new key pair |
| Security Group | Custom SG |

---

# 🔐 EC2 Security Group Rules

## Inbound Rules

| Type | Port | Source |
|---|---|---|
| SSH | 22 | My IP |
| Custom TCP | 5000 | Anywhere |

## Outbound Rules

| Type | Port | Destination |
|---|---|---|
| All Traffic | All | 0.0.0.0/0 |

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

- SSH port 22 was not allowed in Security Group inbound rules.

## Fix

Added:

| Type | Port | Source |
|---|---|---|
| SSH | 22 | My IP |

---

# 🔥 STEP 3 — Update Ubuntu Server

```bash
sudo apt update
sudo apt upgrade -y
```

---

# ❌ ISSUE FACED — APT Repository Connection Error

## Error

```text
Unable to connect to eu-north-1.ec2.archive.ubuntu.com
```

## Root Cause

- EC2 outbound internet access issue
- Incorrect networking setup in old EC2 instance

## Fix

- Deleted broken EC2
- Created fresh EC2 instance
- Verified outbound rule:

```text
All Traffic → 0.0.0.0/0
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

# 🔥 STEP 6 — Create Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# 🔥 STEP 7 — Install Python Packages

```bash
pip install flask flask-cors mysql-connector-python
```

---

# 🔥 STEP 8 — Create Flask App

```bash
nano app.py
```

---

# ❌ ISSUE FACED — Mistaken Terminal Input

## Error

```text
db_config = {...}
Command 'db_config' not found
```

## Root Cause

Python code was typed directly into Linux terminal instead of inside app.py.

## Fix

Opened:

```bash
nano app.py
```

and pasted code inside the file.

---

# 🔥 STEP 9 — Run Flask App

```bash
python3 app.py
```

---

# 🔥 STEP 10 — Open Flask API in Browser

```text
http://EC2-PUBLIC-IP:5000
```

## Output

```json
{
  "message": "Flask API is running!"
}
```

---

# 🔥 STEP 11 — Create RDS MySQL Database

## RDS Configuration

| Setting | Value |
|---|---|
| Engine | MySQL |
| Deployment | Free Tier |
| Public Access | Yes |
| DB Instance Identifier | database-2 |
| Username | admin |
| Password | Custom password |

---

# ❌ ISSUE FACED — Security Group Not Showing

## Problem

Could not see EC2 Security Group while configuring RDS.

## Root Cause

Wrong VPC selection / old deleted resources.

## Fix

Created fresh RDS in same VPC as EC2.

---

# 🔥 STEP 12 — Configure RDS Security Group

## Inbound Rules

| Type | Port | Source |
|---|---|---|
| MySQL/Aurora | 3306 | EC2 Security Group |

---

# ❌ ISSUE FACED — Database Connection Timeout

## Error

```text
Can't connect to MySQL server on port 3306
```

## Root Cause

RDS inbound rule missing.

## Fix

Allowed MySQL port 3306 from EC2 Security Group.

---

# ❌ ISSUE FACED — Unknown Database

## Error

```text
Unknown database 'database-2'
```

## Root Cause

`database-2` is RDS instance name, NOT actual MySQL database name.

## Fix

Created actual MySQL database manually.

---

# 🔥 STEP 13 — Install MySQL Client

```bash
sudo apt install mysql-client -y
```

---

# ❌ ISSUE FACED — Package Not Available

## Error

```text
Package mysql-client-core-8.0 is not available
```

## Fix

Installed:

```bash
sudo apt install mysql-client -y
```

---

# 🔥 STEP 14 — Connect to RDS

```bash
mysql -h RDS-ENDPOINT -u admin -p
```

---

# ❌ ISSUE FACED — SSL Error

## Error

```text
TLS/SSL error: self-signed certificate
```

## Root Cause

MySQL client SSL mismatch.

## Fix

Used SSL disabled configuration inside Flask app.

---

# 🔥 STEP 15 — Create Database

Inside MySQL:

```sql
CREATE DATABASE flaskdb;
SHOW DATABASES;
EXIT;
```

---

# 🔥 STEP 16 — Configure Flask Database Connection

## app.py Database Config

```python
db_config = {
    "host": "RDS-ENDPOINT",
    "user": "admin",
    "password": "YOUR_PASSWORD",
    "database": "flaskdb",
    "ssl_disabled": True
}
```

---

# ❌ ISSUE FACED — Access Denied to mysql Database

## Error

```text
Access denied for user 'admin' to database 'mysql'
```

## Root Cause

Attempted to use AWS system database.

## Fix

Created custom database:

```sql
CREATE DATABASE flaskdb;
```

and updated Flask config.

---

# 🔥 STEP 17 — Final Flask API Features

## Features

- Add User
- Fetch Users
- Store Data in RDS
- REST API
- JSON Responses

---

# 🔥 STEP 18 — Frontend Development

## Frontend Files

- index.html
- style.css
- script.js

---

# 🔥 STEP 19 — Configure Frontend API URL

Inside script.js:

```javascript
const API_URL = "http://EC2-PUBLIC-IP:5000";
```

---

# 🔥 STEP 20 — Upload Frontend to S3

## S3 Configuration

| Setting | Value |
|---|---|
| Static Website Hosting | Enabled |
| Public Access | Enabled |

Uploaded:
- index.html
- style.css
- script.js

---

# 🔥 STEP 21 — Enable Bucket Policy

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

# 🎉 FRONTEND OUTPUT

```text
AWS 3-Tier Architecture Project
Enter Name
Enter Email
Add User
Users List
```

---

# 🔥 STEP 22 — Configure CloudFront CDN

## CloudFront Settings

| Setting | Value |
|---|---|
| Origin | S3 Bucket |
| Viewer Protocol | Redirect HTTP to HTTPS |
| Default Root Object | index.html |

---

# ❌ ISSUE FACED — Access Denied

## Root Cause

`index.html` not configured as default root object.

## Fix

Added:

```text
index.html
```

inside CloudFront settings.

---

# 🎉 FINAL WORKING FLOW

```text
User
   ↓
CloudFront
   ↓
S3 Frontend
   ↓
Flask API on EC2
   ↓
RDS MySQL
```

---

# 🎉 FINAL OUTPUT

```text
Avinash - avinash@test.com
```

---

# 🔥 STEP 23 — CloudWatch Monitoring

## Configured

- CPU Monitoring
- EC2 Metrics
- CloudWatch Alarm

---

# CloudWatch Alarm

| Metric | Threshold |
|---|---|
| CPUUtilization | >70% |

---

# 🔥 STEP 24 — IAM Role & Policies

## Created IAM Role

```text
EC2-CloudWatch-Role
```

## Attached Policies

- CloudWatchAgentServerPolicy
- Custom-S3-Read-Policy

---

# 🔥 Custom IAM Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "S3ReadOnlyAccess",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::*"
      ]
    }
  ]
}
```

---

# 🔥 STEP 25 — Git & GitHub Setup

## Initialize Git

```bash
git init
```

---

## Add Files

```bash
git add .
```

---

## Commit

```bash
git commit -m "Initial commit - AWS 3 tier architecture"
```

---

# ❌ ISSUE FACED — GitHub Authentication Failed

## Error

```text
Invalid username or token
Password authentication is not supported
```

## Root Cause

GitHub no longer supports password authentication.

## Fix

Created GitHub Personal Access Token (PAT) and used token instead of password.

---

# 🎯 Key Learnings

## AWS Skills

- EC2 deployment
- RDS connectivity
- S3 hosting
- CloudFront CDN
- CloudWatch monitoring
- IAM roles & policies
- Security Groups
- Networking basics

---

## DevOps Skills

- Git & GitHub
- Linux commands
- Flask deployment
- REST API development
- Debugging production issues

---

# 🔥 Challenges Solved

| Problem | Solution |
|---|---|
| SSH failed | Fixed SG inbound rule |
| Apt repository failed | Recreated EC2 |
| RDS timeout | Opened port 3306 |
| Unknown database | Created actual DB |
| GitHub auth failed | Used PAT token |
| CloudFront access denied | Added index.html |
| SSL issue | Disabled SSL in Flask |

---

# 🚀 Future Improvements

- Application Load Balancer (ALB)
- Auto Scaling Group
- Multi-AZ RDS
- Bastion Host
- Private Subnets
- NAT Gateway
- Docker
- Terraform
- CI/CD Pipeline
- Kubernetes

---

# 🧠 Interview Questions Covered

- What is 3-tier architecture?
- Why use CloudFront?
- Why use RDS?
- Difference between public/private subnet?
- What are Security Groups?
- Why IAM Roles?
- How frontend communicates with backend?
- What challenges did you face?

---

# 👨‍💻 Author

## Avinash Pandey

AWS | DevOps | Cloud Computing | Python Flask

---

# ⭐ Final Result

Successfully built and deployed a complete production-style AWS 3-tier architecture application using AWS cloud services and DevOps best practices.
