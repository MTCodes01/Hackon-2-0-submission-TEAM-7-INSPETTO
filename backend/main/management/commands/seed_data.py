from django.core.management.base import BaseCommand
from datetime import datetime
from main.models import Camera, Vehicle, Violation, VehicleDocument, VehicleRouteLog, ScanLog, Hub, HubLog
import json

class Command(BaseCommand):
    help = "Load mock data into the database"

    def handle(self, *args, **kwargs):
        with open('D:\Github\Hackon-2-0-submission-TEAM-7-INSPETTO\mock_data.json', 'r') as f:
            mock_data = json.load(f)

        # Insert Cameras
        for cam in mock_data["cameras"]:
            Camera.objects.update_or_create(
                cam_id=cam["cam_id"],
                defaults={
                    "location_name": cam["location_name"],
                    "coordinates": cam["coordinates"],
                    "image_thumbnail": cam["image_thumbnail"]
                }
            )

        # Insert Vehicles
        for v in mock_data["vehicles"]:
            Vehicle.objects.update_or_create(
                chip_id=v["chip_id"],
                defaults={
                    "plate_no": v["plate_no"],
                    "chassis_no": v["chassis_no"],
                    "owner_name": v["owner_name"],
                    "model": v["model"]
                }
            )

        # Insert Violations
        for v in mock_data["violations"]:
            vehicle = Vehicle.objects.get(chip_id=v["chip_id"])
            cam = Camera.objects.get(cam_id=v["cam_id"])
            Violation.objects.create(
                chip=vehicle,
                cam=cam,
                timestamp=v["timestamp"],
                type=v["type"],
                image_proof=v["image_proof"],
                reviewed=v["reviewed"]
            )

        # Insert Vehicle Documents
        for doc in mock_data["vehicle_documents"]:
            vehicle = Vehicle.objects.get(chip_id=doc["chip_id"])
            VehicleDocument.objects.update_or_create(
                chip=vehicle,
                defaults={
                    "fitness_status": doc["fitness_status"],
                    "insurance_status": doc["insurance_status"],
                    "puc_status": doc["puc_status"],
                    "last_checked": doc["last_checked"]
                }
            )

        # Insert Vehicle Route Logs
        for log in mock_data["vehicle_route_logs"]:
            vehicle = Vehicle.objects.get(chip_id=log["chip_id"])
            cam = Camera.objects.get(cam_id=log["cam_id"])
            VehicleRouteLog.objects.create(
                chip=vehicle,
                cam=cam,
                timestamp=log["timestamp"]
            )

        # Insert Scan Logs
        for scan in mock_data["scan_logs"]:
            cam = Camera.objects.get(cam_id=scan["cam_id"])
            ScanLog.objects.create(
                plate_no=scan["plate_no"],
                cam=cam,
                confidence=scan["confidence"],
                timestamp=scan["timestamp"],
                plate_image=scan["plate_image"]
            )

        # Insert Hubs
        for h in mock_data["hubs"]:
            cam = Camera.objects.get(cam_id=h["cam_id"])
            Hub.objects.update_or_create(
                hub_id=h["hub_id"],
                defaults={
                    "cam": cam,
                    "timestamp": h["timestamp"]
                }
            )

        # Insert Hub Logs
        for log in mock_data["hub_logs"]:
            vehicle = Vehicle.objects.get(chip_id=log["chip_id"])
            hub = Hub.objects.get(hub_id=log["hub_id"])
            HubLog.objects.create(
                hub=hub,
                chip=vehicle,
                rssi=log["rssi"],
                timestamp=log["timestamp"]
            )

        self.stdout.write(self.style.SUCCESS("✅ Mock data inserted into database."))
