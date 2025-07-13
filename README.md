# INSPETTO
<p style="font-style=italics;">Made for HACKON 2.0, MCET, Anad</p>

INSPETTO is a cutting-edge surveillance solution designed to **detect tampered or illegal vehicle number plates** using computer vision, OCR, and beacon-based verification. It enables law enforcement agencies to track and verify vehicles in real-time with high accuracy.

Live Demo: [https://inspetto.ceal.in](https://inspetto.ceal.in)

---

## 📦 Features

- 🔍 Real-time license plate detection using OCR  
- 🧠 Automatic classification: **valid**, **tampered**, or **illegal format**  
- 📡 Beacon-chip verification using hardware hubs  
- 🗃️ Centralized database with camera logs, violations, and vehicle data  
- 🌐 REST API for data access and integration  
- 📊 Web dashboard for law enforcement monitoring  

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/MTCodes01/Inspetto-team-7.git
cd Inspetto-team-7
```

### 2. Install Python Dependencies

Ensure Python 3.10+ is installed.

```bash
pip install -r requirements.txt
```

### 3. Start the Application

```bash
start.bat
```

To begin OCR detection:

```bash
cd backend
python OCRing.py
```

> INSPETTO captures plates from your **webcam**. Simply show a number plate image to simulate detection.

---

## 🎥 Input Source & Usage

- Accepts **live video feed** from a webcam  
- Uses `pytesseract` to extract plate numbers from frames  
- Beacon hubs detect the **chip ID** inside nearby vehicles  
- Both logs are sent to the backend for verification  

---

## 🧠 How It Works – Classification Logic

| Step | Action |
|------|--------|
| 1 | Camera captures license plate and OCR extracts plate number |
| 2 | Hub reads Bluetooth beacon inside vehicle (`chip_id`) |
| 3 | Server cross-verifies plate number and chip against DB |
| 4 | System classifies plate as one of the following: |

### Classification Rules

| Type            | Criteria                                                                 |
|------------------|--------------------------------------------------------------------------|
| ✅ Valid          | Plate matches regex + high OCR confidence + beacon ID is linked         |
| ⚠️ Tampered       | Valid-looking plate but mismatched/missing beacon                      |
| 🚫 Illegal Format | Plate doesn't match official regex pattern                             |
| ❓ Low Confidence | OCR confidence below threshold (e.g., `< 70%`)                          |

---

## 🗃️ Database Schema

INSPETTO uses **MySQL** to manage vehicle, camera, and violation data.

### Key Tables

- `users` – officer login system  
- `cameras` – camera location and metadata  
- `vehicles` – plate, chassis, and owner data  
- `violations` – logged anomalies  
- `hubs`, `hub_logs` – beacon-based location tracking  
- `scan_logs` – OCR scan history  
- `vehicle_documents`, `vehicle_route_logs` – registration and movement history  

Example from `scan_logs`:
```sql
scan_id INT PRIMARY KEY AUTO_INCREMENT
plate_no VARCHAR(20)
cam_id VARCHAR(20)
confidence FLOAT
timestamp DATETIME
plate_image BLOB
```

---

## 🔌 API Usage

📍 Base URL: `https://django-api.sreedevss.me/api/`

### REST Endpoints

| Resource           | Endpoint Path          | Method(s)     |
|--------------------|------------------------|---------------|
| Users              | `/users/`              | GET, POST     |
| Cameras            | `/cameras/`            | GET, POST     |
| Vehicles           | `/vehicles/`           | GET, POST     |
| Violations         | `/violations/`         | GET, POST     |
| Hubs               | `/hubs/`               | GET, POST     |
| Scan Logs          | `/scan-logs/`          | GET, POST     |
| Hub Logs           | `/hub-logs/`           | GET, POST     |
| Vehicle Documents  | `/documents/`          | GET, POST     |
| Route Logs         | `/route-logs/`         | GET, POST     |

### Custom Routes

| Path                            | Description                                 |
|----------------------------------|---------------------------------------------|
| `/login/`                        | Login endpoint for officers                 |
| `/cameras/<camID>/`             | Get violation count per camera              |
| `/violations/<camID>/`          | Detailed violations from a specific camera  |
| `/vehicles/<chipID>/`           | Vehicle details from beacon chip ID         |

---

## 👮 Law Enforcement Interface

Web dashboard at [inspetto.ceal.in](https://inspetto.ceal.in) provides:

- 📍 Live scan monitoring  
- 🚦 Violation feed per camera  
- 🧾 Vehicle and route log search  
- 👁️ Role-based officer login (currently read-only)  

> Action-based features (e.g. reviewing violations) are planned for future versions.

---

## 🧪 Testing & Simulation

You can simulate detection without hardware.

### Simulate OCR

1. Open a plate image on your phone or screen  
2. Run the OCR script and hold the plate in front of the webcam

### Simulate Beacon + Data

```bash
python backend/layout-db.py  # creates tables
python manage.py seed_data   # seeds with test entries
```

Make sure to edit your DB credentials in the source code before running.

---

## ⚙️ Configuration

INSPETTO does **not yet use `.env` files**. All sensitive settings (e.g. DB credentials) must be manually edited in:

- `backend/layout-db.py`  
- `seed_data.py`

### Future Recommendation

Switch to `.env` + `python-dotenv` to manage credentials and environment settings securely.

---

## 📄 License

This project is licensed under the **MIT License** — see [`LICENSE`](LICENSE) for details.

---

## 🤝 Contributing

We welcome your contributions to enhance INSPETTO!

### How to Contribute

1. Fork this repository  
2. Create your feature branch: `git checkout -b feature/your-feature-name`  
3. Commit your changes  
4. Push to the branch  
5. Open a pull request  

A `CONTRIBUTING.md` file will be added soon with formatting rules, setup tips, and PR guidelines.

---

## 📋 Requirements

Here’s the `requirements.txt`:

```txt
Django==4.2.5
opencv-python==4.9.0.80
numpy==1.26.4
pytesseract==0.3.10
Pillow==10.3.0
requests==2.31.0
djangorestframework==3.14.0
python-dotenv==1.0.1
mysql-connector-python==8.4.0
aiohttp==3.9.5
```
