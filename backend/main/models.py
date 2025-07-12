from django.db import models


class User(models.Model):
    uid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    password_hash = models.TextField()
    role = models.CharField(max_length=50, default='officer')

    class Meta:
        managed = False
        db_table = 'users'


class Camera(models.Model):
    cam_id = models.CharField(max_length=20, primary_key=True)
    location_name = models.CharField(max_length=100)
    coordinates = models.CharField(max_length=100)
    image_thumbnail = models.TextField()

    class Meta:
        managed = False
        db_table = 'cameras'


class Hub(models.Model):
    hub_id = models.CharField(max_length=20, primary_key=True)
    cam = models.ForeignKey(Camera, on_delete=models.CASCADE, db_column='cam_id')
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'hubs'


class Vehicle(models.Model):
    chip_id = models.CharField(max_length=40, primary_key=True)
    plate_no = models.CharField(max_length=20)
    chassis_no = models.CharField(max_length=30)
    owner_name = models.CharField(max_length=100)
    model = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'vehicles'


class Violation(models.Model):
    violation_id = models.AutoField(primary_key=True)
    chip = models.ForeignKey(Vehicle, on_delete=models.CASCADE, db_column='chip_id')
    cam = models.ForeignKey(Camera, on_delete=models.CASCADE, db_column='cam_id')
    timestamp = models.DateTimeField()
    type = models.CharField(max_length=50)
    image_proof = models.TextField()
    reviewed = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'violations'


class VehicleDocument(models.Model):
    chip = models.OneToOneField(Vehicle, on_delete=models.CASCADE, db_column='chip_id', primary_key=True)
    fitness_status = models.CharField(max_length=20)
    insurance_status = models.CharField(max_length=20)
    puc_status = models.CharField(max_length=20)
    last_checked = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'vehicle_documents'


class VehicleRouteLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    chip = models.ForeignKey(Vehicle, on_delete=models.CASCADE, db_column='chip_id')
    cam = models.ForeignKey(Camera, on_delete=models.CASCADE, db_column='cam_id')
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'vehicle_route_logs'


class ScanLog(models.Model):
    scan_id = models.AutoField(primary_key=True)
    plate_no = models.CharField(max_length=20)
    cam = models.ForeignKey(Camera, on_delete=models.CASCADE, db_column='cam_id')
    confidence = models.FloatField()
    timestamp = models.DateTimeField()
    plate_image = models.BinaryField()

    class Meta:
        managed = False
        db_table = 'Scan_logs'


class HubLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE, db_column='hub_id')
    chip = models.ForeignKey(Vehicle, on_delete=models.CASCADE, db_column='chip_id')
    rssi = models.IntegerField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'hub_logs'
