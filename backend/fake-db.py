import random
from faker import Faker
from datetime import datetime, timedelta
import json

def print_sample_data(data):
    """Print sample data for verification"""
    print("=== SAMPLE MOCK DATA ===\n")
    
    print("Cameras (first 3):")
    for i, camera in enumerate(data['cameras'][:3]):
        print(f"  {i+1}. {camera}")
    
    print(f"\nVehicles (first 3 out of {len(data['vehicles'])}):")
    for i, vehicle in enumerate(data['vehicles'][:3]):
        print(f"  {i+1}. {vehicle}")
    
    print(f"\nViolations (first 3 out of {len(data['violations'])}):")
    for i, violation in enumerate(data['violations'][:3]):
        print(f"  {i+1}. {violation}")
    
    print(f"\nData summary:")
    for table_name, table_data in data.items():
        print(f"  {table_name}: {len(table_data)} records")

def demonstrate_relationships(data):
    """Demonstrate the relationships between tables"""
    print("\n=== RELATIONSHIP DEMONSTRATIONS ===\n")
    
    # Pick a random vehicle and show all related records
    sample_vehicle = random.choice(data['vehicles'])
    print(f"Sample Vehicle: {sample_vehicle['owner_name']} owns {sample_vehicle['model']}")
    print(f"  Chip ID: {sample_vehicle['chip_id']}")
    print(f"  Plate: {sample_vehicle['plate_no']}")
    print(f"  Chassis: {sample_vehicle['chassis_no']}")
    
    # Find related vehicle documents
    vehicle_docs = [doc for doc in data['vehicle_documents'] if doc['chip_id'] == sample_vehicle['chip_id']]
    if vehicle_docs:
        doc = vehicle_docs[0]
        print(f"\n  Document Status:")
        print(f"    Fitness: {doc['fitness_status']}")
        print(f"    Insurance: {doc['insurance_status']}")
        print(f"    PUC: {doc['puc_status']}")
        print(f"    Last Checked: {doc['last_checked']}")
    
    # Find related violations
    violations = [v for v in data['violations'] if v['chip_id'] == sample_vehicle['chip_id']]
    print(f"\n  Violations ({len(violations)} total):")
    for i, violation in enumerate(violations[:3]):  # Show first 3
        cam_location = next((c['location_name'] for c in data['cameras'] if c['cam_id'] == violation['cam_id']), 'Unknown')
        print(f"    {i+1}. {violation['type']} at {cam_location} on {violation['timestamp']}")
    
    # Find related route logs
    route_logs = [log for log in data['vehicle_route_logs'] if log['chip_id'] == sample_vehicle['chip_id']]
    print(f"\n  Route History ({len(route_logs)} locations visited):")
    for i, log in enumerate(route_logs[:3]):  # Show first 3
        cam_location = next((c['location_name'] for c in data['cameras'] if c['cam_id'] == log['cam_id']), 'Unknown')
        print(f"    {i+1}. Visited {cam_location} on {log['timestamp']}")
    
    # Find related scan logs
    scan_logs = [log for log in data['scan_logs'] if log['plate_no'] == sample_vehicle['plate_no']]
    print(f"\n  Plate Scans ({len(scan_logs)} scans):")
    for i, log in enumerate(scan_logs[:3]):  # Show first 3
        cam_location = next((c['location_name'] for c in data['cameras'] if c['cam_id'] == log['cam_id']), 'Unknown')
        print(f"    {i+1}. Scanned at {cam_location} on {log['timestamp']} (confidence: {log['confidence']})")
    
    # Find related hub logs
    hub_logs = [log for log in data['hub_logs'] if log['chip_id'] == sample_vehicle['chip_id']]
    print(f"\n  Hub Detections ({len(hub_logs)} detections):")
    for i, log in enumerate(hub_logs[:3]):  # Show first 3
        hub_cam = next((h['cam_id'] for h in data['hubs'] if h['hub_id'] == log['hub_id']), 'Unknown')
        cam_location = next((c['location_name'] for c in data['cameras'] if c['cam_id'] == hub_cam), 'Unknown')
        print(f"    {i+1}. Detected by {log['hub_id']} near {cam_location} on {log['timestamp']} (RSSI: {log['rssi']})")
    
    # Show relationship integrity
    print(f"\n=== RELATIONSHIP INTEGRITY CHECK ===")
    print(f"Total vehicles: {len(data['vehicles'])}")
    print(f"Vehicle documents: {len(data['vehicle_documents'])} (should match vehicles)")
    print(f"Violations reference valid vehicles: {len([v for v in data['violations'] if any(vehicle['chip_id'] == v['chip_id'] for vehicle in data['vehicles'])])} / {len(data['violations'])}")
    print(f"Scan logs reference valid plates: {len([s for s in data['scan_logs'] if any(vehicle['plate_no'] == s['plate_no'] for vehicle in data['vehicles'])])} / {len(data['scan_logs'])}")
    print(f"Hub logs reference valid vehicles: {len([h for h in data['hub_logs'] if any(vehicle['chip_id'] == h['chip_id'] for vehicle in data['vehicles'])])} / {len(data['hub_logs'])}")

def demonstrate_relationships(data):
    """Demonstrate the relationships between tables"""
    print("\n=== RELATIONSHIP DEMONSTRATIONS ===\n")
    
    # Pick a random vehicle and show all related records
    sample_vehicle = random.choice(data['vehicles'])
    print(f"Sample Vehicle: {sample_vehicle['owner_name']} owns {sample_vehicle['model']}")
    print(f"  Chip ID: {sample_vehicle['chip_id']}")
    print(f"  Plate: {sample_vehicle['plate_no']}")
    print(f"  Chassis: {sample_vehicle['chassis_no']}")
    
    # Find related vehicle documents
    vehicle_docs = [doc for doc in data['vehicle_documents'] if doc['chip_id'] == sample_vehicle['chip_id']]
    if vehicle_docs:
        doc = vehicle_docs[0]
        print(f"\n  Document Status:")
        print(f"    Fitness: {doc['fitness_status']}")
        print(f"    Insurance: {doc['insurance_status']}")
        print(f"    PUC: {doc['puc_status']}")
        print(f"    Last Checked: {doc['last_checked']}")
    
    # Find related violations
    violations = [v for v in data['violations'] if v['chip_id'] == sample_vehicle['chip_id']]
    print(f"\n  Violations ({len(violations)} total):")
    for i, violation in enumerate(violations[:3]):  # Show first 3
        cam_location = next((c['location_name'] for c in data['cameras'] if c['cam_id'] == violation['cam_id']), 'Unknown')
        print(f"    {i+1}. {violation['type']} at {cam_location} on {violation['timestamp']}")
    
    # Find related route logs
    route_logs = [log for log in data['vehicle_route_logs'] if log['chip_id'] == sample_vehicle['chip_id']]
    print(f"\n  Route History ({len(route_logs)} locations visited):")
    for i, log in enumerate(route_logs[:3]):  # Show first 3
        cam_location = next((c['location_name'] for c in data['cameras'] if c['cam_id'] == log['cam_id']), 'Unknown')
        print(f"    {i+1}. Visited {cam_location} on {log['timestamp']}")
    
    # Find related scan logs
    scan_logs = [log for log in data['scan_logs'] if log['plate_no'] == sample_vehicle['plate_no']]
    print(f"\n  Plate Scans ({len(scan_logs)} scans):")
    for i, log in enumerate(scan_logs[:3]):  # Show first 3
        cam_location = next((c['location_name'] for c in data['cameras'] if c['cam_id'] == log['cam_id']), 'Unknown')
        print(f"    {i+1}. Scanned at {cam_location} on {log['timestamp']} (confidence: {log['confidence']})")
    
    # Find related hub logs
    hub_logs = [log for log in data['hub_logs'] if log['chip_id'] == sample_vehicle['chip_id']]
    print(f"\n  Hub Detections ({len(hub_logs)} detections):")
    for i, log in enumerate(hub_logs[:3]):  # Show first 3
        hub_cam = next((h['cam_id'] for h in data['hubs'] if h['hub_id'] == log['hub_id']), 'Unknown')
        cam_location = next((c['location_name'] for c in data['cameras'] if c['cam_id'] == hub_cam), 'Unknown')
        print(f"    {i+1}. Detected by {log['hub_id']} near {cam_location} on {log['timestamp']} (RSSI: {log['rssi']})")
    
    # Show relationship integrity
    print(f"\n=== RELATIONSHIP INTEGRITY CHECK ===")
    print(f"Total vehicles: {len(data['vehicles'])}")
    print(f"Vehicle documents: {len(data['vehicle_documents'])} (should match vehicles)")
    print(f"Violations reference valid vehicles: {len([v for v in data['violations'] if any(vehicle['chip_id'] == v['chip_id'] for vehicle in data['vehicles'])])} / {len(data['violations'])}")
    print(f"Scan logs reference valid plates: {len([s for s in data['scan_logs'] if any(vehicle['plate_no'] == s['plate_no'] for vehicle in data['vehicles'])])} / {len(data['scan_logs'])}")
    print(f"Hub logs reference valid vehicles: {len([h for h in data['hub_logs'] if any(vehicle['chip_id'] == h['chip_id'] for vehicle in data['vehicles'])])} / {len(data['hub_logs'])}")

# Initialize Faker
fake = Faker('en_IN')  # Using Indian locale for more realistic data

# Bangalore specific locations for cameras
bangalore_locations = [
    "MG Road, Bangalore",
    "Brigade Road, Bangalore", 
    "Residency Road, Bangalore",
    "Commercial Street, Bangalore",
    "Koramangala, Bangalore",
    "Indiranagar, Bangalore",
    "Whitefield, Bangalore",
    "Electronic City, Bangalore",
    "Marathahalli, Bangalore",
    "BTM Layout, Bangalore",
    "Jayanagar, Bangalore",
    "Malleshwaram, Bangalore",
    "Rajajinagar, Bangalore",
    "Hebbal, Bangalore",
    "Banashankari, Bangalore",
    "HSR Layout, Bangalore",
    "Yelahanka, Bangalore",
    "Sarjapur Road, Bangalore",
    "Bannerghatta Road, Bangalore",
    "Outer Ring Road, Bangalore"
]

# Indian state codes for license plates
state_codes = ['KA', 'KL', 'TN', 'AP', 'TS', 'MH', 'DL', 'RJ', 'UP', 'GJ', 'HR', 'PB', 'WB', 'OR', 'MP']

# Vehicle models
vehicle_models = [
    'Maruti Swift', 'Hyundai i20', 'Honda City', 'Maruti Baleno', 'Tata Nexon',
    'Mahindra XUV300', 'Kia Seltos', 'Hyundai Creta', 'Maruti Ertiga', 'Toyota Innova',
    'Mahindra Scorpio', 'Ford EcoSport', 'Renault Duster', 'Nissan Magnite', 'MG Hector',
    'Tata Harrier', 'Jeep Compass', 'Skoda Rapid', 'Volkswagen Polo', 'BMW 3 Series',
    'Audi A4', 'Mercedes C-Class', 'Honda WR-V', 'Maruti Vitara Brezza', 'Hyundai Venue'
]

def generate_plate_number():
    """Generate realistic Indian license plate number"""
    state = random.choice(state_codes)
    district = random.randint(1, 99)
    letters = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=2))
    numbers = random.randint(1000, 9999)
    return f"{state} {district:02d} {letters} {numbers}"

def generate_chip_id():
    """Generate realistic chip ID"""
    return fake.hexify(text='^^^^^^^^^^^^', upper=True)

def generate_cam_id():
    """Generate camera ID"""
    return f"CAM{random.randint(1000, 9999)}"

def generate_hub_id():
    """Generate hub ID"""
    return f"hub{fake.hexify(text='^^^^^^^^^^^^', upper=True)}"

def generate_coordinates():
    """Generate realistic Bangalore coordinates"""
    # Bangalore approximate bounds
    lat = round(random.uniform(12.8, 13.2), 6)
    lon = round(random.uniform(77.4, 77.8), 6)
    return f"{lat}, {lon}"

def generate_chassis_number():
    """Generate realistic chassis number"""
    return fake.bothify(text='MA1??2??K#?######', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ')

def generate_mock_data():
    """Generate complete mock data for all tables with strong relationships"""
    
    # Generate cameras data first
    cameras = []
    cam_ids = []
    
    for i in range(20):  # Generate 20 cameras
        cam_id = generate_cam_id()
        cam_ids.append(cam_id)
        
        camera = {
            "cam_id": cam_id,
            "location_name": random.choice(bangalore_locations),
            "coordinates": generate_coordinates(),
            "image_thumbnail": f"camera_{cam_id.lower()}_thumbnail.jpg"
        }
        cameras.append(camera)
    
    # Generate hubs data (linked to cameras)
    hubs = []
    hub_ids = []
    
    for i in range(15):  # Generate 15 hubs
        hub_id = generate_hub_id()
        hub_ids.append(hub_id)
        
        hub = {
            "hub_id": hub_id,
            "cam_id": random.choice(cam_ids),
            "timestamp": fake.date_time_between(start_date='-30d', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
        }
        hubs.append(hub)
    
    # Generate vehicles data (core entities)
    vehicles = []
    vehicle_lookup = {}  # For quick lookup: chip_id -> vehicle data
    
    for i in range(100):  # Generate 100 vehicles
        chip_id = generate_chip_id()
        plate_no = generate_plate_number()
        owner_name = fake.name()
        model = random.choice(vehicle_models)
        
        vehicle = {
            "chip_id": chip_id,
            "plate_no": plate_no,
            "chassis_no": generate_chassis_number(),
            "owner_name": owner_name,
            "model": model
        }
        vehicles.append(vehicle)
        
        # Store in lookup for relationship building
        vehicle_lookup[chip_id] = {
            "plate_no": plate_no,
            "owner_name": owner_name,
            "model": model
        }
    
    # Generate vehicle documents (one-to-one with vehicles)
    vehicle_documents = []
    document_statuses = ['Valid', 'Expired', 'Pending', 'Not Available']
    
    for vehicle in vehicles:
        # Create realistic document status relationships
        fitness_status = random.choice(document_statuses)
        insurance_status = random.choice(document_statuses)
        puc_status = random.choice(document_statuses)
        
        # If vehicle has expired documents, higher chance of violations
        vehicle_lookup[vehicle['chip_id']]['document_risk'] = (
            fitness_status == 'Expired' or 
            insurance_status == 'Expired' or 
            puc_status == 'Expired'
        )
        
        doc = {
            "chip_id": vehicle['chip_id'],
            "fitness_status": fitness_status,
            "insurance_status": insurance_status,
            "puc_status": puc_status,
            "last_checked": fake.date_time_between(start_date='-90d', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
        }
        vehicle_documents.append(doc)
    
    # Generate realistic vehicle route logs (vehicle journeys)
    vehicle_route_logs = []
    
    # Create realistic journeys for each vehicle
    for vehicle in vehicles:
        # Each vehicle has 3-8 location visits in the last 30 days
        num_visits = random.randint(3, 8)
        
        for _ in range(num_visits):
            log = {
                "chip_id": vehicle['chip_id'],
                "cam_id": random.choice(cam_ids),
                "timestamp": fake.date_time_between(start_date='-30d', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
            }
            vehicle_route_logs.append(log)
    
    # Generate violations (linked to vehicles with higher risk)
    violations = []
    violation_types = [
        'Speed Limit Violation', 'Red Light Violation', 'Wrong Lane', 
        'No Helmet', 'Triple Riding', 'Parking Violation', 'Signal Jump',
        'Overloading', 'Document Missing', 'Rash Driving'
    ]
    
    # Create violations with realistic patterns
    for i in range(200):
        # Higher chance of violations for vehicles with expired documents
        if random.random() < 0.3:  # 30% chance to pick high-risk vehicle
            high_risk_vehicles = [v for v in vehicles if vehicle_lookup[v['chip_id']].get('document_risk', False)]
            if high_risk_vehicles:
                selected_vehicle = random.choice(high_risk_vehicles)
            else:
                selected_vehicle = random.choice(vehicles)
        else:
            selected_vehicle = random.choice(vehicles)
        
        # If vehicle has expired documents, more likely to have "Document Missing" violation
        if vehicle_lookup[selected_vehicle['chip_id']].get('document_risk', False) and random.random() < 0.4:
            violation_type = 'Document Missing'
        else:
            violation_type = random.choice(violation_types)
        
        violation = {
            "chip_id": selected_vehicle['chip_id'],
            "cam_id": random.choice(cam_ids),
            "timestamp": fake.date_time_between(start_date='-7d', end_date='now').strftime('%Y-%m-%d %H:%M:%S'),
            "type": violation_type,
            "image_proof": f"violation_{i+1}_proof.jpg",
            "reviewed": random.choice([True, False])
        }
        violations.append(violation)
    
    # Generate scan logs (linked to actual vehicle plates)
    scan_logs = []
    
    for i in range(300):
        # Pick a random vehicle and use its actual plate number
        vehicle = random.choice(vehicles)
        
        log = {
            "plate_no": vehicle['plate_no'],
            "cam_id": random.choice(cam_ids),
            "confidence": round(random.uniform(0.7, 0.99), 3),
            "timestamp": fake.date_time_between(start_date='-7d', end_date='now').strftime('%Y-%m-%d %H:%M:%S'),
            "plate_image": f"plate_scan_{i+1}.jpg"
        }
        scan_logs.append(log)
    
    # Generate hub logs (linked to actual vehicles and hubs)
    hub_logs = []
    
    for i in range(400):
        # Pick a random vehicle and hub
        vehicle = random.choice(vehicles)
        hub = random.choice(hubs)
        
        log = {
            "hub_id": hub['hub_id'],
            "chip_id": vehicle['chip_id'],
            "rssi": random.randint(-100, -30),
            "timestamp": fake.date_time_between(start_date='-7d', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
        }
        hub_logs.append(log)
    
    # Compile all data
    mock_data = {
        "cameras": cameras,
        "hubs": hubs,
        "vehicles": vehicles,
        "violations": violations,
        "vehicle_documents": vehicle_documents,
        "vehicle_route_logs": vehicle_route_logs,
        "scan_logs": scan_logs,
        "hub_logs": hub_logs
    }
    
    return mock_data

def save_to_json(data, filename="mock_data.json"):
    """Save mock data to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Mock data saved to {filename}")

def print_sample_data(data):
    """Print sample data for verification"""
    print("=== SAMPLE MOCK DATA ===\n")
    
    print("Cameras (first 3):")
    for i, camera in enumerate(data['cameras'][:3]):
        print(f"  {i+1}. {camera}")
    
    print(f"\nVehicles (first 3 out of {len(data['vehicles'])}):")
    for i, vehicle in enumerate(data['vehicles'][:3]):
        print(f"  {i+1}. {vehicle}")
    
    print(f"\nViolations (first 3 out of {len(data['violations'])}):")
    for i, violation in enumerate(data['violations'][:3]):
        print(f"  {i+1}. {violation}")
    
    print(f"\nData summary:")
    for table_name, table_data in data.items():
        print(f"  {table_name}: {len(table_data)} records")

if __name__ == "__main__":
    # Generate mock data
    print("Generating mock data...")
    mock_data = generate_mock_data()
    
    # Print sample data
    print_sample_data(mock_data)
    
    # Demonstrate relationships
    demonstrate_relationships(mock_data)
    
    # Save to JSON file
    save_to_json(mock_data)
    
    print("\n=== Mock data generation completed! ===")
    print("Key features of the generated data:")
    print("✓ All foreign key relationships are intact")
    print("✓ Vehicle documents exist for every vehicle")
    print("✓ Violations reference actual vehicles and cameras")
    print("✓ Scan logs use actual vehicle plate numbers")
    print("✓ Hub logs reference actual vehicles and hubs")
    print("✓ Route logs show realistic vehicle movement patterns")
    print("✓ Vehicles with expired documents have higher violation rates")
    print("✓ Document violations are more common for vehicles with expired papers")