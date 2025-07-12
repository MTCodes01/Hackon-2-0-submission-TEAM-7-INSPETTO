import cv2
import pytesseract
import numpy as np
import re
from collections import deque
import time
import math
import csv
import os
import datetime

# 📍 Tesseract Path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
state_codes = [
    'AP', 'AR', 'AS', 'BR', 'CG', 'CH', 'DD', 'DL', 'DN', 'GA', 'GJ', 'HP',
    'HR', 'JH', 'JK', 'KA', 'KL', 'LA', 'LD', 'MH', 'ML', 'MN', 'MP', 'MZ',
    'NL', 'OD', 'PB', 'PY', 'RJ', 'SK', 'TN', 'TR', 'TS', 'UK', 'UP', 'WB'
]

# More flexible pattern to match Indian license plates
# Format: State code (2 letters), followed by 1-2 digits, followed by 1-3 letters, followed by 1-4 digits
# This allows for formats like "TN 11 C 5369" after cleaning
plate_pattern = r'^(' + '|'.join(state_codes) + r')\s*\d{1,2}\s*[A-Z]{1,3}\s*\d{1,4}'
plate_regex = re.compile(plate_pattern)

STABILITY_THRESHOLD = 5
CONFIDENCE_THRESHOLD = 55
COOLDOWN_PERIOD = 5.0  # Increased to avoid re-detecting the same plate too soon
RESULT_BUFFER_SIZE = 5  # Number of OCR results to consider
MAX_OCR_ATTEMPTS = 5    # Maximum number of OCR attempts before concluding
MAX_PLATES_TO_STORE = 5  # Number of most recent plates to store and save to CSV
CSV_FILENAME = "detected_plates.csv"  # Name of the CSV file to save detections

# Camera metadata constants
CAM_ID = "0001"
LOCATION_NAME = "attingal"
COORDINATES = "700,800"

def validate_plate_with_regex(text):
    """
    Validates if the text represents a valid Indian license plate format.
    Only accepts plates that strictly start with valid state codes.
    Handles various real-world formats including spaces between components.
    """
    if not text:
        return None
    
    # First, convert to uppercase and remove any leading/trailing whitespace
    text = text.upper().strip()
    
    # Check if the text starts with a valid state code (with possible spaces)
    found_state_code = None
    for state_code in state_codes:
        if text.startswith(state_code) or text.startswith(state_code + ' '):
            found_state_code = state_code
            break
    
    if not found_state_code:
        return None
    
    # Clean the text while preserving spaces for proper pattern matching
    clean_text = ''.join(c if c.isalnum() or c.isspace() else ' ' for c in text).upper()
    # Replace multiple spaces with single space
    clean_text = ' '.join(clean_text.split())
    
    # Try matching with spaces preserved
    match = plate_regex.search(clean_text)
    if match:
        # Format the result with consistent spacing for display
        matched_text = match.group(0)
        # Remove all spaces to get clean alphanumeric text
        alphanumeric_only = ''.join(c for c in matched_text if c.isalnum())
        
        # Format for consistent display: XX 00 X 0000
        if len(alphanumeric_only) >= 4:  # Must have at least state code + some digits
            state = alphanumeric_only[:2]
            rest = alphanumeric_only[2:]
            
            # Extract components (district code, series, number)
            district_end = 0
            for i, char in enumerate(rest):
                if not char.isdigit():
                    district_end = i
                    break
            
            if district_end > 0:
                district = rest[:district_end]
                remaining = rest[district_end:]
                
                series_end = 0
                for i, char in enumerate(remaining):
                    if char.isdigit():
                        series_end = i
                        break
                
                if series_end > 0:
                    series = remaining[:series_end]
                    number = remaining[series_end:]
                    
                    # Return formatted plate
                    return f"{state} {district} {series} {number}"
                
            # Fallback if we can't properly segment
            return alphanumeric_only
    
    # If we have a state code but no full match, try a more permissive check
    # This helps with partial or unusual formats that still have valid state codes
    if found_state_code and len(clean_text) >= 4:  # At least need state + some identifier
        # Keep only alphanumeric characters
        alphanumeric_only = ''.join(c for c in clean_text if c.isalnum())
        
        # Check if we have digits and letters after the state code
        rest = alphanumeric_only[2:]
        has_digit = any(c.isdigit() for c in rest)
        has_letter = any(c.isalpha() for c in rest)
        
        # If we have both digits and letters after the state code, it's probably a valid plate
        if has_digit and has_letter:
            # Try to format it
            state = alphanumeric_only[:2]
            
            # Simple attempt to separate components
            district = ''
            series = ''
            number = ''
            
            current_part = ''
            current_type = None  # 0 for digit, 1 for letter
            
            for c in rest:
                new_type = 1 if c.isalpha() else 0
                
                if current_type is None:
                    current_type = new_type
                    current_part += c
                elif current_type == new_type:
                    current_part += c
                else:
                    # Type changed
                    if current_type == 0:  # Was digit, now letter
                        if not district:
                            district = current_part
                        else:
                            number = current_part
                    else:  # Was letter, now digit
                        series = current_part
                    
                    current_part = c
                    current_type = new_type
            
            # Handle the last part
            if current_part:
                if current_type == 0:  # Digit
                    if not district:
                        district = current_part
                    else:
                        number = current_part
                else:  # Letter
                    series = current_part
            
            # Return formatted result
            if district and series and number:
                return f"{state} {district} {series} {number}"
            return alphanumeric_only
    
    return None

def detect_license_plate(image):
    # Create a copy of the original image
    working_image = image.copy()
    
    # Convert to grayscale
    gray = cv2.cvtColor(working_image, cv2.COLOR_BGR2GRAY)
    
    # Step 1: Adaptive histogram equalization
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    
    # Step 2: Bilateral filtering for noise reduction
    blurred = cv2.bilateralFilter(enhanced, 11, 17, 17)
    
    # Step 3: Edge detection with adaptive thresholds
    avg_intensity = np.mean(blurred)
    low_thresh = max(10, avg_intensity * 0.5)
    high_thresh = min(200, avg_intensity * 2)
    edges = cv2.Canny(blurred, low_thresh, high_thresh)
    
    # Step 4: Morphological operations to close gaps
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    
    # Find contours
    contours, _ = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    
    plate_candidates = []
    
    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.03 * peri, True)
        
        # Accept both 4-sided and 4+ sided contours
        if len(approx) >= 4:
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = w / float(h)
            
            # Calculate solidity (area vs convex hull area)
            hull = cv2.convexHull(contour)
            hull_area = cv2.contourArea(hull)
            if hull_area > 0:
                solidity = cv2.contourArea(contour) / hull_area
            else:
                solidity = 0
            
            # Check if contour meets plate characteristics
            if (2.0 <= aspect_ratio <= 5.5 and 
                w > 80 and h > 30 and 
                0.7 <= solidity <= 1.0):
                
                # Calculate rotated rectangle
                rect = cv2.minAreaRect(contour)
                box = cv2.boxPoints(rect)
                box = box.astype(np.int32)
                
                # Calculate extent (contour area vs bounding box area)
                rect_area = w * h
                extent = cv2.contourArea(contour) / rect_area if rect_area > 0 else 0
                
                if extent > 0.6:
                    plate_candidates.append((contour, box, rect, extent))
    
    # Sort candidates by extent
    plate_candidates.sort(key=lambda x: x[3], reverse=True)
    
    if plate_candidates:
        # Get the best candidate
        contour, box, rect, extent = plate_candidates[0]
        
        # Warp perspective to correct rotation
        plate_img = four_point_transform(working_image, box)
        return plate_img, cv2.boundingRect(contour)
    
    return None, None

def order_points(pts):
    """Order points clockwise starting from top-left"""
    # Initialize list of coordinates
    rect = np.zeros((4, 2), dtype="float32")
    
    # The top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    
    # Compute the difference between the points
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    
    return rect


def four_point_transform(image, pts):
    """Apply perspective transform to license plate"""
    # Order points consistently
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    
    # Compute width of new image
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    
    # Compute height of new image
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    
    # Create destination points
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")
    
    # Compute perspective transform matrix
    M = cv2.getPerspectiveTransform(rect, dst)
    
    # Apply warp perspective
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    
    return warped

def preprocess_license_plate(image):
    if image is None or image.size == 0:
        return None
        
    # Standardize size - maintain aspect ratio but make it larger for better OCR
    height = 120  # Increased from 70 for better OCR
    aspect_ratio = image.shape[1] / float(image.shape[0])
    width = int(height * aspect_ratio)
    resized = cv2.resize(image, (width, height))
    
    # Convert to grayscale
    if len(resized.shape) == 3:
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    else:
        gray = resized
    
    # Apply CLAHE in all cases - helps with various lighting
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    
    # Create multiple processing variants for better OCR results
    # 1. Adaptive thresholding - binary inverse
    thresh_inv = cv2.adaptiveThreshold(
        enhanced, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 11, 2
    )
    
    # 2. Adaptive thresholding - regular binary (light text on dark background)
    thresh_reg = cv2.adaptiveThreshold(
        enhanced, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )
    
    # 3. Otsu's thresholding
    _, otsu = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # 4. Apply blur to reduce noise
    blur = cv2.GaussianBlur(enhanced, (5, 5), 0)
    _, otsu_blur = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Morphological operations to clean text for each variant
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    cleaned_inv = cv2.morphologyEx(thresh_inv, cv2.MORPH_CLOSE, kernel)
    cleaned_reg = cv2.morphologyEx(thresh_reg, cv2.MORPH_CLOSE, kernel)
    cleaned_otsu = cv2.morphologyEx(otsu, cv2.MORPH_CLOSE, kernel)
    cleaned_otsu_blur = cv2.morphologyEx(otsu_blur, cv2.MORPH_CLOSE, kernel)
    
    # Return all variants and the enhanced grayscale for OCR attempts
    return {
        'gray': enhanced,  # Enhanced grayscale
        'inv': cleaned_inv,  # Inverse binary
        'reg': cleaned_reg,  # Regular binary
        'otsu': cleaned_otsu,  # Otsu threshold
        'otsu_blur': cleaned_otsu_blur  # Otsu with blur
    }

def extract_plate_text_and_confidence(images):
    if images is None:
        return "", 0.0
    
    # PSM modes to try for better OCR
    psm_modes = [
        7,  # Treat image as a single text line
        8,  # Treat image as a single word
        6,  # Assume a single uniform block of text
        3   # Fully automatic page segmentation without orientation and script detection
    ]
    
    # OCR engine modes to try
    oem_modes = [3, 1]  # 3 = Default, 1 = Neural nets LSTM only
    
    best_results = []  # Store all results to choose the best one
    
    # Try OCR on each image variant with different configurations
    for img_name, img in images.items():
        if img is None or img.size == 0:
            continue
            
        for psm in psm_modes:
            for oem in oem_modes:
                config = f'--oem {oem} --psm {psm} -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 '
                
                try:
                    # Try both image_to_data and image_to_string for comparison
                    data = pytesseract.image_to_data(
                        img,
                        config=config,
                        output_type=pytesseract.Output.DICT
                    )
                    
                    # Direct string method often gives cleaner results
                    direct_string = pytesseract.image_to_string(img, config=config).strip()
                    
                    text_list = []
                    confidences = []
                    
                    for i in range(len(data['text'])):
                        word = data['text'][i].strip()
                        if word:
                            try:
                                conf = float(data['conf'][i])
                                if conf > 0:
                                    text_list.append(word)
                                    confidences.append(conf)
                            except:
                                continue
                    
                    # Get text from data method
                    data_text = ' '.join(text_list)
                    avg_conf = sum(confidences) / len(confidences) if confidences else 0.0
                    
                    # Print debug info for each attempt
                    if data_text or direct_string:
                        print(f"[🔬] OCR [{img_name} PSM{psm} OEM{oem}] | Data: '{data_text}' ({avg_conf:.1f}%) | String: '{direct_string}'")
                    
                    # Add both methods to results
                    if data_text:
                        best_results.append((data_text, avg_conf, f"{img_name}-data-psm{psm}-oem{oem}"))
                    if direct_string:
                        # Assign a confidence based on string length as image_to_string doesn't provide conf
                        str_conf = min(90.0, len(direct_string) * 5)  # Longer strings get higher confidence
                        best_results.append((direct_string, str_conf, f"{img_name}-string-psm{psm}-oem{oem}"))
                        
                except Exception as e:
                    print(f"[⚠️] OCR error with {img_name}, PSM{psm}, OEM{oem}: {str(e)}")
    
    if not best_results:
        return "", 0.0
    
    # Choose the best result based on whether it contains a valid plate format
    valid_results = []
    for text, conf, method in best_results:
        # Try to validate the plate format
        valid_plate = validate_plate_with_regex(text)
        if valid_plate:
            valid_results.append((valid_plate, conf, method, True))
        else:
            valid_results.append((text, conf, method, False))
    
    # Sort first by validity, then by confidence
    valid_results.sort(key=lambda x: (x[3], x[1]), reverse=True)
    
    # Get the best result
    if valid_results:
        best_text, best_conf, method, valid = valid_results[0]
        print(f"[🏆] Best OCR result: '{best_text}' ({best_conf:.1f}%) [Method: {method}, Valid: {valid}]")
        return best_text, best_conf
    
    return "", 0.0

def is_same_plate(plate1, plate2):
    """Check if two plates are similar (allowing OCR errors)"""
    if not plate1 or not plate2:
        return False
        
    clean1 = ''.join(filter(str.isalnum, plate1))
    clean2 = ''.join(filter(str.isalnum, plate2))
    
    # If plates are exact match after cleaning
    if clean1 == clean2:
        return True
        
    # If plates are the same length, allow 1 character difference
    if len(clean1) == len(clean2):
        diff_count = sum(1 for a, b in zip(clean1, clean2) if a != b)
        return diff_count <= 1
    
    # If different lengths, check if one is substring of the other
    if len(clean1) > len(clean2):
        return clean2 in clean1
    else:
        return clean1 in clean2

def save_to_csv(valid_plate, filename=CSV_FILENAME):
    """
    Save the detected license plates to a CSV file
    
    Args:
        plates_data: List of tuples (plate_number, confidence, timestamp)
        filename: Name of the CSV file to save to
    """
    # Always use write mode to rewrite the entire file with all plates
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['cam_id', 'location_name', 'coordinates', 'number_plate', 'confidence', 'timestamp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the data rows
        for plate, conf, timestamp in valid_plate:
            writer.writerow({
                'cam_id': CAM_ID,
                'location_name': LOCATION_NAME,
                'coordinates': COORDINATES,
                'number_plate': plate,
                'confidence': conf,
                'timestamp': timestamp
            })
    
    print(f"[💾] Saved {len(valid_plate)} license plate(s) to {filename}")

def main():
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Error: Could not open camera")
        return
        
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("🚗 Starting automatic license plate scanner")
    print("❌ Press 'q' to quit")
    print(f"📊 Will store up to {MAX_PLATES_TO_STORE} plates in {CSV_FILENAME}")
    
    # Data structure to store detected plates
    detected_plates = []  # List of tuples (plate_number, confidence, timestamp)
    
    last_valid_plate = None
    last_scan_time = 0
    detection_history = deque(maxlen=STABILITY_THRESHOLD)
    result_buffer = deque(maxlen=RESULT_BUFFER_SIZE)  # Buffer for OCR results
    ocr_attempt_count = 0  # Counter for OCR attempts
    processing_plate = False  # Flag to indicate if we're currently processing a plate
    
    for _ in range(STABILITY_THRESHOLD):
        detection_history.append(False)
        
    while True:
        start_time = time.time()
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to capture frame")
            break
            
        processed_frame = cv2.resize(frame, (320, 240))
        current_time = time.time()
        on_cooldown = (current_time - last_scan_time) < COOLDOWN_PERIOD
        
        plate_region, bbox = detect_license_plate(processed_frame)
        has_detection = plate_region is not None
        
        if has_detection:
            # Draw bounding box on original frame
            x, y, w, h = bbox
            scale_x = frame.shape[1] / processed_frame.shape[1]
            scale_y = frame.shape[0] / processed_frame.shape[0]
            orig_x = int(x * scale_x)
            orig_y = int(y * scale_y)
            orig_w = int(w * scale_x)
            orig_h = int(h * scale_y)
            
            cv2.rectangle(frame, (orig_x, orig_y), (orig_x + orig_w, orig_y + orig_h), (0, 255, 0), 2)
            cv2.putText(frame, "License Plate Detected", (orig_x, orig_y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            detection_history.append(True)
            
            if (sum(detection_history) >= STABILITY_THRESHOLD and 
                not on_cooldown and 
                plate_region is not None):
                
                # Get multiple processed variants
                processed_variants = preprocess_license_plate(plate_region)
                
                # Show processed plate variants for debugging
                if processed_variants is not None:
                    # Display the original plate
                    cv2.imshow("Original Plate", plate_region)
                    
                    # Display each variant in its own window
                    for name, img in processed_variants.items():
                        if img is not None:
                            cv2.imshow(f"Processed Plate - {name}", img)
                
                # Perform OCR on all variants
                text, conf = extract_plate_text_and_confidence(processed_variants)
                
                # Always try to find a valid plate in the OCR text
                valid_plate = validate_plate_with_regex(text)
                
                if valid_plate and conf >= CONFIDENCE_THRESHOLD:
                    # Add to result buffer
                    result_buffer.append((valid_plate, conf))
                    print(f"[📝] Added to buffer: {valid_plate} (Conf: {conf:.1f}%)")
                    ocr_attempt_count += 1
                    print(f"[🔢] OCR attempt {ocr_attempt_count} of {MAX_OCR_ATTEMPTS}")
                elif text:
                    print(f"[⚠️] OCR: {text} (Conf: {conf:.1f}%)")
                    if valid_plate:
                        # If we found a valid plate after cleanup, add it to the buffer
                        result_buffer.append((valid_plate, conf))
                        print(f"[🔍] Found valid plate format after cleanup: {valid_plate}")
                        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        save_to_csv([(valid_plate, conf, timestamp)], CSV_FILENAME)
                        print(f"[📝] Saved single detection: {valid_plate} (Conf: {conf:.1f}%)")

                        ocr_attempt_count += 1
                        print(f"[🔢] OCR attempt {ocr_attempt_count} of {MAX_OCR_ATTEMPTS}")
                    else:
                        # Count this as an attempt even if no valid plate was found
                        ocr_attempt_count += 1
                        print(f"[🔢] OCR attempt {ocr_attempt_count} of {MAX_OCR_ATTEMPTS} (No valid plate)")

                    
                
                # Process buffer when we have enough OCR attempts
                if ocr_attempt_count >= MAX_OCR_ATTEMPTS:
                    plate_counter = {}
                    plate_confidences = {}
                    
                    # Aggregate results by plate
                    for plate, conf in result_buffer:
                        if plate not in plate_counter:
                            plate_counter[plate] = 0
                            plate_confidences[plate] = []
                        plate_counter[plate] += 1
                        plate_confidences[plate].append(conf)
                    
                    # Prioritize by frequency and confidence
                    if plate_counter:
                        # Get plates with at least 2 detections
                        valid_candidates = {plate: count for plate, count in plate_counter.items()
                                           if count >= 2}
                        
                        if valid_candidates:
                            # Sort candidates by confidence if they have enough detections
                            candidates_with_conf = []
                            for plate, count in valid_candidates.items():
                                avg_conf = sum(plate_confidences[plate]) / len(plate_confidences[plate])
                                if avg_conf >= CONFIDENCE_THRESHOLD:
                                    candidates_with_conf.append((plate, count, avg_conf))
                            
                            # Sort by confidence first, then by frequency
                            if candidates_with_conf:
                                candidates_with_conf.sort(key=lambda x: (x[2], x[1]), reverse=True)
                                best_plate, count, avg_conf = candidates_with_conf[0]
                                
                                # Check if this is a new plate (not a duplicate of recent detections)
                                is_duplicate = False
                                for plate_info in detected_plates:
                                    if is_same_plate(plate_info[0], best_plate):
                                        is_duplicate = True
                                        break
                                
                                # Only accept if we have a valid candidate and it's not a duplicate
                                if not is_duplicate:
                                    print(f"\n[🔍] Buffer Analysis:")
                                    for plate, confs in plate_confidences.items():
                                        count = plate_counter[plate]
                                        avg = sum(confs) / len(confs)
                                        print(f"  - {plate}: Count={count}, Avg Conf={avg:.1f}%")
                                    
                                    print(f"[✅] Detected Plate: {best_plate} (Avg Conf: {avg_conf:.1f}%)")
                                    
                                    # Add timestamp for this detection
                                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    
                                    # Add to our detected plates list
                                    detected_plates.append((best_plate, avg_conf, timestamp))
                                    
                                    # Keep only the most recent MAX_PLATES_TO_STORE plates
                                    if len(detected_plates) > MAX_PLATES_TO_STORE:
                                        detected_plates = detected_plates[-MAX_PLATES_TO_STORE:]
                                    
                                    # Save all detected plates to CSV
                                    
                                    last_valid_plate = best_plate
                                    last_scan_time = current_time
                                    
                                    # Show the detection on screen
                                    cv2.putText(frame, f"Plate: {best_plate}", (10, 30),
                                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                                    cv2.putText(frame, f"Confidence: {avg_conf:.1f}%", (10, 60),
                                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                                    
                                    # Display the updated count
                                    print(f"[📊] Total unique plates detected: {len(detected_plates)}")
                                    print(f"[🎯] Recent detection: {best_plate} (Confidence: {avg_conf:.1f}%)")
                                else:
                                    print(f"[🔄] Duplicate plate detected: {best_plate} - skipping")
                    
                    # Reset for next plate detection regardless of result
                    result_buffer.clear()
                    ocr_attempt_count = 0
        else:
            detection_history.append(False)
            
        if on_cooldown:
            cooldown_left = COOLDOWN_PERIOD - (current_time - last_scan_time)
            cv2.putText(frame, f"Cooldown: {cooldown_left:.1f}s", (10, frame.shape[0] - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        elif last_valid_plate and not detected_plates:
            # Only show last plate if we don't have a full list yet
            cv2.putText(frame, f"Last Plate: {last_valid_plate}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        # Display recent detections if we have any
        if detected_plates:
            # Create a semi-transparent overlay for the plate list
            overlay = frame.copy()
            cv2.rectangle(overlay, (10, 100), (350, 100 + min(len(detected_plates), 5) * 30 + 40), (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
            
            # Add title for recent detections
            cv2.putText(frame, f"Recent Detections ({len(detected_plates)})", (15, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # List the plates with timestamp
            for i, (plate, conf, timestamp) in enumerate(reversed(detected_plates)):
                if i >= 5:  # Only show up to 5 plates
                    break
                y_pos = 150 + i * 30
                # Get just the time part of the timestamp
                time_only = timestamp.split()[1]
                cv2.putText(frame, f"{i+1}. {plate} ({conf:.1f}%) - {time_only}", (15, y_pos),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
        fps = 1.0 / (time.time() - start_time)
        cv2.putText(frame, f"FPS: {fps:.1f}", (frame.shape[1] - 120, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        cv2.imshow("Automatic License Plate Scanner", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("👋 Exiting...")
            break
            
    cap.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()
