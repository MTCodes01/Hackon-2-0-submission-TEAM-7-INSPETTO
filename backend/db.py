import mysql.connector
from mysql.connector import errorcode
from datetime import datetime

# 1. DATABASE CONNECTION CONFIG
config = {
    'user': 'root',
    'password': 'nandu',  # <--- CHANGE THIS
    'host': 'localhost'
}

DB_NAME = "Inspetto"

# 2. SQL TABLE DEFINITIONS
TABLES = {}

TABLES['users'] = """
CREATE TABLE IF NOT EXISTS users (
    uid VARCHAR(20) PRIMARY KEY,
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
    chip_id VARCHAR(20),
    plate_from_chip VARCHAR(20),
    plate_from_image VARCHAR(20),
    chassis_no VARCHAR(30),
    tampering_detected BOOLEAN,
    reason TEXT,
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
    timestamp DATETIME,
    FOREIGN KEY (chip_id) REFERENCES vehicles(chip_id),
    FOREIGN KEY (hub_id) REFERENCES hubs(hub_id)
);"""

# 3. MOCK DATA
mockData = {
    "cameras": [
        {"id": "CAM001", "location": "MG Road, Bangalore", "coordinates": "12.9716, 77.5946", "image": "placeholder.jpg", "violations": 24},
        {"id": "CAM002", "location": "Brigade Road, Bangalore", "coordinates": "12.9698, 77.6085", "image": "placeholder.jpg", "violations": 18},
        {"id": "CAM003", "location": "Residency Road, Bangalore", "coordinates": "12.9719, 77.5937", "image": "placeholder.jpg", "violations": 31},
        {"id": "CAM004", "location": "Commercial Street, Bangalore", "coordinates": "12.9833, 77.6167", "image": "placeholder.jpg", "violations": 12},
        {"id": "CAM005", "location": "Koramangala, Bangalore", "coordinates": "12.9352, 77.6245", "image": "placeholder.jpg", "violations": 27},
        {"id": "CAM006", "location": "Indiranagar, Bangalore", "coordinates": "12.9784, 77.6408", "image": "placeholder.jpg", "violations": 15},
    ],
    "violations": {
        "CAM001": [
            {"id": 1, "timestamp": "2025-07-12 14:30:00", "beacon": "ABCDEF123456", "plate": "KL 19 ABC", "violations": 8},
            {"id": 2, "timestamp": "2025-07-12 13:45:00", "beacon": "GHIJKL789012", "plate": "KA 05 XYZ", "violations": 3},
            {"id": 3, "timestamp": "2025-07-12 12:20:00", "beacon": "MNOPQR345678", "plate": "TN 32 DEF", "violations": 12},
            {"id": 4, "timestamp": "2025-07-12 11:15:00", "beacon": "STUVWX901234", "plate": "AP 28 GHI", "violations": 5},
            {"id": 5, "timestamp": "2025-07-12 10:30:00", "beacon": "ABCDEF567890", "plate": "KL 08 JKL", "violations": 7},
        ],
        "CAM002": [
            {"id": 1, "timestamp": "2025-07-12 15:20:00", "beacon": "BCDEFG234567", "plate": "KA 01 MNO", "violations": 6},
            {"id": 2, "timestamp": "2025-07-12 14:45:00", "beacon": "HIJKLM890123", "plate": "KL 14 PQR", "violations": 4},
            {"id": 3, "timestamp": "2025-07-12 13:30:00", "beacon": "NOPQRS456789", "plate": "TN 09 STU", "violations": 9},
        ],
    },
    "profiles": {
        "KL 19 ABC": {
            "name": "Rahul Menon",
            "registeredPlates": ["KL 19 ABC", "KL 20 DEF", "KL 19 GHI"],
            "recentScans": [
                {"timestamp": "2025-07-12 14:30:00", "location": "MG Road, Bangalore"},
                {"timestamp": "2025-07-12 09:15:00", "location": "Brigade Road, Bangalore"},
                {"timestamp": "2025-07-11 18:45:00", "location": "Koramangala, Bangalore"},
            ],
        },
        "KA 05 XYZ": {
            "name": "Priya Sharma",
            "registeredPlates": ["KA 05 XYZ", "KA 03 LMN"],
            "recentScans": [
                {"timestamp": "2025-07-12 13:45:00", "location": "MG Road, Bangalore"},
                {"timestamp": "2025-07-12 08:30:00", "location": "Indiranagar, Bangalore"},
            ],
        },
    },
}

# 4. CONNECT AND CREATE DB + TABLES
try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cnx.database = DB_NAME
    for name, ddl in TABLES.items():
        cursor.execute(ddl)
    print("✅ Database and tables ready.")

    # 5. INSERT CAMERA DATA
    for cam in mockData["cameras"]:
        cursor.execute("""
            INSERT INTO cameras (cam_id, location_name, coordinates, image_thumbnail)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE location_name=VALUES(location_name)
        """, (cam["id"], cam["location"], cam["coordinates"], cam["image"]))
    
    # 6. INSERT VIOLATIONS + VEHICLES
    for cam_id, violations in mockData["violations"].items():
        for v in violations:
            cursor.execute("""
                INSERT INTO vehicles (chip_id, plate_no, chassis_no, owner_name, model)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE plate_no=VALUES(plate_no)
            """, (v["beacon"], v["plate"], "CHASSIS123", "Unknown", "Model X"))
            cursor.execute("""
                INSERT INTO violations (chip_id, cam_id, timestamp, type, image_proof, reviewed)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (v["beacon"], cam_id, v["timestamp"], "Plate Mismatch", "placeholder.jpg", False))
    
    # 7. INSERT PROFILE DATA
    for plate, profile in mockData["profiles"].items():
        for reg_plate in profile["registeredPlates"]:
            chip_id = f"{reg_plate.replace(' ', '')}_chip"
            cursor.execute("""
                INSERT INTO vehicles (chip_id, plate_no, chassis_no, owner_name, model)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE owner_name=VALUES(owner_name)
            """, (chip_id, reg_plate, "CHASSIS999", profile["name"], "Generic Car"))
            cursor.execute("""
                INSERT INTO vehicle_documents (chip_id, fitness_status, insurance_status, puc_status, last_checked)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE last_checked=VALUES(last_checked)
            """, (chip_id, "Valid", "Valid", "Expired", datetime.now()))
            for scan in profile["recentScans"]:
                cursor.execute("""
                    INSERT INTO vehicle_route_logs (chip_id, cam_id, timestamp)
                    VALUES (%s, %s, %s)
                """, (chip_id, "CAM001", scan["timestamp"]))  # Simplified cam_id for demo

    cnx.commit()
    cursor.close()
    cnx.close()
    print("✅ Sample data inserted successfully.")

except mysql.connector.Error as err:
    print(f"❌ MySQL error: {err}")
