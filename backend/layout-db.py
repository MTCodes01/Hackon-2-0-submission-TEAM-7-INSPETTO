import mysql.connector
from mysql.connector import errorcode
from datetime import datetime

config = {
    'user': 'root',
    'password': 'password',
    'host': 'localhost'
}

DB_NAME = "Inspetto"

TABLES = {}

TABLES['users'] = """
CREATE TABLE IF NOT EXISTS users (
    uid INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    password_hash TEXT NOT NULL,
    role VARCHAR(50) DEFAULT 'officer'
);"""

TABLES['cameras'] = """
CREATE TABLE IF NOT EXISTS cameras (
    cam_id VARCHAR(20) PRIMARY KEY,
    location_name VARCHAR(100),
    coordinates VARCHAR(100),
    image_thumbnail TEXT
);"""

TABLES['hubs'] = """
CREATE TABLE IF NOT EXISTS hubs (
    hub_id VARCHAR(20) PRIMARY KEY,
    cam_id VARCHAR(20),
    timestamp DATETIME,
    FOREIGN KEY (cam_id) REFERENCES cameras(cam_id)
);"""

TABLES['vehicles'] = """
CREATE TABLE IF NOT EXISTS vehicles (
    chip_id VARCHAR(40) PRIMARY KEY,
    plate_no VARCHAR(20),
    chassis_no VARCHAR(30),
    owner_name VARCHAR(100),
    model VARCHAR(50)
);"""

TABLES['violations'] = """
CREATE TABLE IF NOT EXISTS violations (
    violation_id INT AUTO_INCREMENT PRIMARY KEY,
    chip_id VARCHAR(40),
    cam_id VARCHAR(20),
    timestamp DATETIME,
    type VARCHAR(50),
    image_proof TEXT,
    reviewed BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (chip_id) REFERENCES vehicles(chip_id),
    FOREIGN KEY (cam_id) REFERENCES cameras(cam_id)
);"""

TABLES['vehicle_documents'] = """
CREATE TABLE IF NOT EXISTS vehicle_documents (
    chip_id VARCHAR(40) PRIMARY KEY,
    fitness_status VARCHAR(20),
    insurance_status VARCHAR(20),
    puc_status VARCHAR(20),
    last_checked DATETIME,
    FOREIGN KEY (chip_id) REFERENCES vehicles(chip_id)
);"""

TABLES['vehicle_route_logs'] = """
CREATE TABLE IF NOT EXISTS vehicle_route_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    chip_id VARCHAR(40),
    cam_id VARCHAR(20),
    timestamp DATETIME,
    FOREIGN KEY (chip_id) REFERENCES vehicles(chip_id),
    FOREIGN KEY (cam_id) REFERENCES cameras(cam_id)
);"""

TABLES['Scan_logs'] = """
CREATE TABLE IF NOT EXISTS Scan_logs (
    scan_id INT AUTO_INCREMENT PRIMARY KEY,
    plate_no VARCHAR(20),
    cam_id VARCHAR(20),
    confidence FLOAT,
    timestamp DATETIME,
    plate_image blob,
    FOREIGN KEY (cam_id) REFERENCES cameras(cam_id)
);"""
TABLES['hub_logs'] = """
CREATE TABLE IF NOT EXISTS hub_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    hub_id VARCHAR(40),
    chip_id VARCHAR(20),
    rssi INT,
    timestamp DATETIME,
    FOREIGN KEY (chip_id) REFERENCES vehicles(chip_id),
    FOREIGN KEY (hub_id) REFERENCES hubs(hub_id)
);"""

try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cnx.database = DB_NAME
    for name, ddl in TABLES.items():
        cursor.execute(ddl)
    print("✅ Database and tables ready.")

    cnx.commit()
    cursor.close()
    cnx.close()
    print("✅ Sample data inserted successfully.")

except mysql.connector.Error as err:
    print(f"❌ MySQL error: {err}")
