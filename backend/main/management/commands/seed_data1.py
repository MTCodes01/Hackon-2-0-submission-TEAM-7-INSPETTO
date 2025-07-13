from django.core.management.base import BaseCommand
from datetime import datetime
from main.models import Camera, Vehicle, Violation, VehicleDocument, VehicleRouteLog

class Command(BaseCommand):
    help = 'Seeds the database with mock data'

    def handle(self, *args, **options):
        mockData = {
            "cameras": [
                {"id": "CAM001", "location": "MG Road, Bangalore", "coordinates": "12.9716, 77.5946", "image": "placeholder.jpg"},
                {"id": "CAM002", "location": "Brigade Road, Bangalore", "coordinates": "12.9698, 77.6085", "image": "placeholder.jpg"},
                {"id": "CAM003", "location": "Residency Road, Bangalore", "coordinates": "12.9719, 77.5937", "image": "placeholder.jpg"},
                {"id": "CAM004", "location": "Commercial Street, Bangalore", "coordinates": "12.9833, 77.6167", "image": "placeholder.jpg"},
                {"id": "CAM005", "location": "Koramangala, Bangalore", "coordinates": "12.9352, 77.6245", "image": "placeholder.jpg"},
                {"id": "CAM006", "location": "Indiranagar, Bangalore", "coordinates": "12.9784, 77.6408", "image": "placeholder.jpg"},
            ],
            "violations": {
                "CAM001": [
                    {"id": 1, "timestamp": "2025-07-12 14:30:00", "beacon": "ABCDEF123456", "plate": "KL 19 ABC"},
                    {"id": 2, "timestamp": "2025-07-12 13:45:00", "beacon": "GHIJKL789012", "plate": "KA 05 XYZ"},
                    {"id": 3, "timestamp": "2025-07-12 12:20:00", "beacon": "MNOPQR345678", "plate": "TN 32 DEF"},
                    {"id": 4, "timestamp": "2025-07-12 11:15:00", "beacon": "STUVWX901234", "plate": "AP 28 GHI"},
                    {"id": 5, "timestamp": "2025-07-12 10:30:00", "beacon": "ABCDEF567890", "plate": "KL 08 JKL"},
                ],
                "CAM002": [
                    {"id": 1, "timestamp": "2025-07-12 15:20:00", "beacon": "BCDEFG234567", "plate": "KA 01 MNO"},
                    {"id": 2, "timestamp": "2025-07-12 14:45:00", "beacon": "HIJKLM890123", "plate": "KL 14 PQR"},
                    {"id": 3, "timestamp": "2025-07-12 13:30:00", "beacon": "NOPQRS456789", "plate": "TN 09 STU"},
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
            }
        }

        # Insert Cameras
        for cam in mockData["cameras"]:
            Camera.objects.update_or_create(
                cam_id=cam["id"],
                defaults={
                    "location_name": cam["location"],
                    "coordinates": cam["coordinates"],
                    "image_thumbnail": cam["image"]
                }
            )

        # Insert Violations & Vehicles
        for cam_id, violations in mockData["violations"].items():
            for v in violations:
                vehicle, _ = Vehicle.objects.update_or_create(
                    chip_id=v["beacon"],
                    defaults={
                        "plate_no": v["plate"],
                        "chassis_no": "CHASSIS123",
                        "owner_name": "Unknown",
                        "model": "Model X"
                    }
                )
                Violation.objects.create(
                    chip=vehicle,  # assuming ForeignKey named 'chip' in Violation
                    cam=Camera.objects.get(cam_id=cam_id),  # assuming ForeignKey named 'cam'
                    timestamp=v["timestamp"],
                    type="Plate Mismatch",
                    image_proof="placeholder.jpg",
                    reviewed=False
                )

        # Insert Profiles (Vehicles + Docs + Route Logs)
        for plate, profile in mockData["profiles"].items():
            for reg_plate in profile["registeredPlates"]:
                chip_id = f"{reg_plate.replace(' ', '')}_chip"
                vehicle, _ = Vehicle.objects.update_or_create(
                    chip_id=chip_id,
                    defaults={
                        "plate_no": reg_plate,
                        "chassis_no": "CHASSIS999",
                        "owner_name": profile["name"],
                        "model": "Generic Car"
                    }
                )
                VehicleDocument.objects.update_or_create(
                    chip=vehicle,  # assuming ForeignKey named 'chip'
                    defaults={
                        "fitness_status": "Valid",
                        "insurance_status": "Valid",
                        "puc_status": "Expired",
                        "last_checked": datetime.now()
                    }
                )
                for scan in profile["recentScans"]:
                    VehicleRouteLog.objects.create(
                        chip=vehicle,
                        cam=Camera.objects.get(cam_id="CAM001"),  # Simplified demo logic
                        timestamp=scan["timestamp"]
                    )

        self.stdout.write(self.style.SUCCESS("✅ Mock data inserted into database."))
