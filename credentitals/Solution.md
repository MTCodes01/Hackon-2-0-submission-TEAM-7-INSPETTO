# 🚓 INSPETTO — Smart Tampered Number Plate Detection System using ANPR + AI

INSPETTO is an intelligent, budget-friendly system designed to **detect tampered, hidden, or illegal vehicle number plates** using real-time image recognition, plate behavior analysis, and crowdsourced verification. Unlike traditional ANPR systems that only *read* number plates, INSPETTO goes a step further — it *understands*, *analyzes*, and *flags* anomalies caused by real-world tampering tricks.

---

## 📸 What is ANPR?

**Automatic Number Plate Recognition (ANPR)** is a computer vision-based system that detects and reads vehicle number plates using **Optical Character Recognition (OCR)** from images, often captured by **infrared (IR) cameras**.

### ✅ What ANPR does well:
- Reads clearly visible plates in daylight and at night
- Recognizes characters and logs vehicle entries/exits
- Matches number plates with registered owner databases

### ❌ What ANPR struggles with:
- Fails when plates are:
  - Covered (mud, stickers)
  - Overexposed (reflective film)
  - Illegally formatted (wrong font, spacing)
  - Swapped with fake/duplicate numbers
- Cannot identify plate swaps done before/after camera points
- Struggles in heavy traffic and low-res environments

---

## 💀 Real-World Tampering Tactics

Bad actors manipulate number plates in multiple ways:
1. **Reflective stickers or films** to blind IR cameras
2. **Glow-in-the-dark ink or coatings**
3. **Plate covers or transparent diffusers**
4. **Font and spacing alterations**
5. **Quick plate swaps before and after camera zones**

---

## 🧠 Your Unique Scenario (The Mechanic Trick)

> An expert swaps the tampered plate before the camera, crosses the checkpoint with a clean plate, then swaps back to the tampered plate. Since cameras are few and of low quality, this trick works without detection.

---

## 🔍 INSPETTO’s Smart Solutions

### 1. 🔄 **Plate Swap Frequency Detection**
- Calculates expected travel time between checkpoints
- Flags plates that appear at impossible intervals (too fast or slow)
- Helps detect unrealistic movement patterns

### 2. 🕓 **Temporal Appearance Pattern Detection**
- Tracks plate sightings over days and weeks
- Flags plates that:
  - Only appear once
  - Never show up again in other areas
- Detects “ghost plates” used briefly for illegal purposes

### 3. 🧬 **Vehicle Appearance Verification (Optional)**
- Matches basic vehicle appearance (type, color, shape)
- Detects mismatches using VAHAN data (e.g., plate says "truck" but vehicle is a car)

### 4. 🔦 **Image Forensics using OpenCV + AI**
- Detects:
  - Over-reflective hotspots on number plates
  - Font/spacing irregularities
  - Skewed or suspicious number plate attachments
- Uses:
  - OCR bounding box spacing checks
  - Brightness heatmaps
  - Template matching for fonts

### 5. 🗂️ **Public RTO (VAHAN) Database Cross-verification**
- Matches captured number plate with official vehicle data:
  - Make/model
  - Fuel type
  - Registration zone
- Flags mismatches between plate info and real-world vehicle

### 6. 🧠 **Suspicion Scoring System**
Each passing vehicle is given a **"Suspicion Score" (0–100)** based on:
- Reflection behavior
- Font/spacing integrity
- Travel time anomalies
- VAHAN mismatch
- Inconsistent appearances

Plates crossing a threshold (e.g. 75+) are flagged for manual review or alerts.

---

## 📣 Bonus Feature: Public Crowdsourced Reporting

Let citizens participate in tamper detection!

- A simple web/mobile form to report suspicious number plates
- Users can upload:
  - Plate photo
  - Location
  - Suspected issue (e.g., covered digits)
- Data is logged and used to validate or train the tamper detection model

---

## 🧰 Tech Stack (Suggested)

| Layer | Tools |
|-------|-------|
| 🖼️ Image Processing | OpenCV, Python |
| 🔡 OCR | Tesseract OCR |
| 🤖 AI/ML | YOLOv8, PyTorch/CNN for forensics |
| 🌐 Web UI | React / Flask |
| 🗃️ Database | SQLite / PostgreSQL |
| 🚙 Vehicle Info | VAHAN public API or dataset |
| 👥 Crowdsourcing | Google Forms or Custom App |
| 🧪 Testing | Simulated image datasets of normal & tampered plates |

---

## 🚦 Project Flow (How INSPETTO Works)

1. **Capture IR Image → OCR Extract Plate**
2. **Check for plate clarity, reflectivity, font legality**
3. **Cross-check with RTO (VAHAN) data**
4. **Check behavior patterns over time**
5. **Assign suspicion score**
6. **Raise alert if score crosses threshold**
7. **(Optional) Accept public reports to verify or feed ML model**

---

## 🧪 Dataset Requirements

- Images of:
  - Normal plates (day/night)
  - Tampered plates (covered, reflective, etc.)
- Sample vehicle metadata (type, color, plate)
- Simulated camera logs (plate sightings, timestamps)

---

## 🛡️ Future Extensions

- Real-time video stream processing
- Integration with traffic police portals
- Blockchain-based immutable plate records
- Invisible watermarking of number plates
- Integration with stolen vehicle alert systems

---

## 👤 Author

**Sree**  
B.Tech CSE-AIML student | Hack404 Founder | RAS CEAL Secretary  
Project under hackathon theme: **Vehicle Safety & Legal Compliance**

---

## 🏁 Conclusion

**INSPETTO isn't just another number plate reader.**  
It is a system that thinks like a criminal — and catches them at their own game.  
It uses **behavioral analysis**, **forensics**, and **public participation** to identify vehicle tampering **without expensive hardware**.  
It’s affordable, scalable, and built for the real-world challenges we face in India.

---

---

## 👥 User Roles & Use Cases

INSPETTO is built for **two distinct user types**, each with tailored features and access:

---

### 👮‍♂️ 1. Law Enforcement Officers

**Purpose:** Monitor vehicle movement, detect tampered number plates, take action.

**Features Available:**
- Secure officer login with credentials
- Dashboard showing:
  - List of detected tampered plates
  - Time and location of detection
  - Tampering type (reflective, swapped, altered font, etc.)
  - Vehicle details from VAHAN (Make, Model, Type, Color, Fuel Type)
  - Owner information
  - Vehicle history:
    - Number of tampering attempts
    - Any linked criminal records
    - Past traffic violations
- Exportable reports for action and legal use
- Alert system for repeated offenders or blacklisted numbers
- Review queue of crowd-reported cases (see Use Case 2)

---

### 🙋‍♀️ 2. General Public / Citizens

**Purpose:** Empower citizens to report suspicious or tampered vehicle number plates.

**Features Available:**
- Open/public web/mobile interface
- Anonymous or optional login
- Upload form to submit:
  - Photo of suspected vehicle
  - Location & time
  - Short description or suspicion type (e.g. covered plate, shiny plate)
- Submission goes to a **review queue** for officers
- Citizens can view their submitted reports and status (e.g., “Under Review,” “Flagged,” “Cleared”)

---

### 🔄 Public–Officer Interaction Flow

1. Public reports a suspicious vehicle.
2. Officers receive it in their dashboard under “Public Reports.”
3. Officer verifies the data using:
   - Internal detection system
   - RTO database
   - Prior vehicle history
4. If confirmed → flagged for field investigation / legal notice.

---
