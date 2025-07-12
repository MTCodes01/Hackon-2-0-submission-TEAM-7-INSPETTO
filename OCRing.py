import cv2
import pytesseract
import numpy as np
import re

# 📍 Tesseract Path
pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract-OCR\tesseract.exe'

# ✅ All valid Indian state codes (2-letter)
state_codes = [
    'AP', 'AR', 'AS', 'BR', 'CG', 'CH', 'DD', 'DL', 'DN', 'GA', 'GJ', 'HP',
    'HR', 'JH', 'JK', 'KA', 'KL', 'LA', 'LD', 'MH', 'ML', 'MN', 'MP', 'MZ',
    'NL', 'OD', 'PB', 'PY', 'RJ', 'SK', 'TN', 'TR', 'TS', 'UK', 'UP', 'WB'
]

# ✅ Compile regex pattern for valid license plates
plate_regex = re.compile(r'^(' + '|'.join(state_codes) + r')\d{2}[A-Z]{1,2}\d{4}$')

def validate_plate_with_regex(text):
    """Checks if a plate is in valid Indian format."""
    return bool(plate_regex.match(text))

def detect_license_plate(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    filtered = cv2.bilateralFilter(gray, 11, 17, 17)
    edges = cv2.Canny(filtered, 30, 200)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.018 * peri, True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = w / h
            if 2.0 <= aspect_ratio <= 5.5 and w > 100 and h > 30:
                return image[y:y+h, x:x+w], (x, y, w, h)
    return None, None

def preprocess_license_plate(image):
    if image is None:
        return None
    if image.shape[0] < 50:
        image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(
        blurred, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )
    return thresh

def extract_plate_text_and_confidence(image):
    if image is None:
        return "", 0.0

    # Try different PSM modes to improve OCR
    configs = [
        r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
        r'--oem 3 --psm 7',
        r'--oem 3 --psm 11',
    ]

    best_text = ""
    best_conf = 0.0

    for config in configs:
        data = pytesseract.image_to_data(image, config=config, output_type=pytesseract.Output.DICT)
        text_list = []
        confidences = []

        for i in range(len(data['text'])):
            word = data['text'][i].strip()
            try:
                conf = float(data['conf'][i])
            except:
                conf = 0

            if word and conf > 30:
                text_list.append(word)
                confidences.append(conf)

        final_text = ''.join(filter(str.isalnum, ''.join(text_list))).upper()
        avg_conf = sum(confidences) / len(confidences) if confidences else 0.0

        if avg_conf > best_conf:
            best_conf = avg_conf
            best_text = final_text

    return best_text, best_conf

def find_valid_plate_by_trimming(text):
    """Trim characters from the start until a valid Indian plate format is matched."""
    for i in range(len(text)):
        trimmed = text[i:]
        if plate_regex.match(trimmed):
            return trimmed
    return None



def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    print("📸 Press 's' to scan")
    print("❌ Press 'q' to quit")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame.")
            break

        plate_region, bbox = detect_license_plate(frame)

        if bbox:
            x, y, w, h = bbox
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "License Plate Detected", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow("Live - Press 's' to scan", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):
            if plate_region is not None:
                processed = preprocess_license_plate(plate_region)
                cv2.imshow("Processed", processed)

                text, conf = extract_plate_text_and_confidence(processed)

                if text:
                    valid_plate = find_valid_plate_by_trimming(text)

                    if valid_plate:
                        print(f"\n[🔍] Extracted Plate: {valid_plate}")
                        print(f"[📏] Confidence: {conf:.2f}%")
                        print(f"[✅] Format Match: ✔ Valid")
                    else:
                        print(f"\n[⚠️] Ignored Text (Invalid Format): {text}")
                else:
                    print("❌ No text detected.")

            else:
                print("❌ No license plate region detected.")

        elif key == ord('q'):
            print("👋 Exiting...")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
