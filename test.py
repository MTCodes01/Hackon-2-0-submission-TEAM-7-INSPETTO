import re

indian_vehicle_regex = {
    "standard": r"^[A-Z]{2}[-\s]?\d{1,2}[-\s]?[A-Z]{1,3}[-\s]?\d{4}$",
    "temporary": r"^TEMP[-\s]?[A-Z]{2}[-\s]?\d{1,2}[-\s]?\d{4}$",
    "military": r"^\d{2}-[A-Z]{1,3}-\d{4,5}$",  # e.g., 22-K-12345
    "diplomatic": r"^([0-9]{2})[-\s]?([A-Z]{1,3})[-\s]?([0-9]{1,4})$",  # e.g., 45 UN 14
    "vintage": r"^VT[-\s]?[A-Z]{2}[-\s]?\d{1,2}[-\s]?[A-Z]{1,3}[-\s]?\d{4}$",  # tentative format
    "electric": r"^[A-Z]{2}[-\s]?\d{1,2}[-\s]?[A-Z]{1,3}[-\s]?\d{4}[E|e]?$",
    "rental": r"^[A-Z]{2}[-\s]?\d{1,2}[-\s]?[A-Z]{1,3}[-\s]?\d{4}$",  # color-based (yellow)
    "transport": r"^[A-Z]{2}[-\s]?\d{1,2}[-\s]?[A-Z]{1,3}[-\s]?\d{4}$",  # color-based (black/yellow)
    "government": r"^IND[-\s]?[A-Z]{2}[-\s]?\d{1,2}[-\s]?[A-Z]{1,3}[-\s]?\d{4}$",  # optional "IND"
    "police": r"^[A-Z]{2}[-\s]?\d{1,2}[-\s]?[P]{1}[A-Z]{0,2}[-\s]?\d{4}$",  # e.g., KL-07-PA-1234
    "dealer": r"^DLR[-\s]?[A-Z]{2}[-\s]?\d{1,2}[-\s]?[A-Z]{1,2}[-\s]?\d{4}$"
}

plate = "KL-07-PA-1234"
matched = False
for category, pattern in indian_vehicle_regex.items():
    if re.match(pattern, plate):
        print(f"Matched category: {category}")
        matched = True
        break

if not matched:
    print("No category matched.")