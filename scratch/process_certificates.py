import os
import cv2
import numpy as np
import easyocr

print("Initializing EasyOCR reader...")
reader = easyocr.Reader(['en', 'ar'], gpu=False)

raw_dir = r'C:\Users\user\Desktop\arwad-certificates\jpg'
out_dir = r'C:\Users\user\Desktop\arwad-portfolio\assets\certificates'
os.makedirs(out_dir, exist_ok=True)

files = sorted([f for f in os.listdir(raw_dir) if f.endswith('.jpg')])

keywords = [
    "certificate", "appreciation", "participation", "attendance", "awarded", "present",
    "ieee", "google", "arwad", "alomosh", "university", "completion", "contest",
    "workshop", "leadership", "event", "robot", "sumo", "course", "training", "honor"
]

def rotate_image(img, angle):
    if angle == 90:
        return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    elif angle == 180:
        return cv2.rotate(img, cv2.ROTATE_180)
    elif angle == 270:
        return cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return img

def get_best_rotation(img):
    best_angle = 0
    max_score = -1
    best_results = []
    
    # Downscale for fast OCR testing
    h, w = img.shape[:2]
    scale = 800 / max(h, w)
    small_img = cv2.resize(img, (int(w * scale), int(h * scale)))
    
    for angle in [0, 90, 180, 270]:
        rotated = rotate_image(small_img, angle)
        # Read text
        results = reader.readtext(rotated)
        
        # Calculate score based on text length and keyword matches
        score = 0
        for bbox, text, prob in results:
            if prob > 0.2:
                score += len(text) * prob
                text_lower = text.lower()
                for kw in keywords:
                    if kw in text_lower:
                        score += 50 * prob
                        
        if score > max_score:
            max_score = score
            best_angle = angle
            best_results = results
            
    return best_angle, best_results

def crop_certificate_background(img):
    # img is rotated upright
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Blur and threshold to find bright paper area
    blurred = cv2.GaussianBlur(gray, (9, 9), 0)
    
    # Try Otsu thresholding or high intensity thresholding
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    best_box = None
    max_area = 0
    img_area = h * w
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 0.25 * img_area:
            x, y, bw, bh = cv2.boundingRect(cnt)
            if area > max_area:
                max_area = area
                best_box = (x, y, bw, bh)
                
    if best_box is not None:
        x, y, bw, bh = best_box
        # Add slight padding or trim margin (ensure we stay within bounds)
        pad_x = int(bw * 0.01)
        pad_y = int(bh * 0.01)
        
        x1 = max(0, x + pad_x)
        y1 = max(0, y + pad_y)
        x2 = min(w, x + bw - pad_x)
        y2 = min(h, y + bh - pad_y)
        
        # Only crop if valid dimensions
        if (x2 - x1) > 0.4 * w and (y2 - y1) > 0.4 * h:
            cropped = img[y1:y2, x1:x2]
            return cropped
            
    # Fallback smart crop: crop 5% from edges if contour failed
    crop_h = int(h * 0.04)
    crop_w = int(w * 0.04)
    return img[crop_h:h-crop_h, crop_w:w-crop_w]

summary = []

for filename in files:
    filepath = os.path.join(raw_dir, filename)
    img = cv2.imread(filepath)
    if img is None:
        continue
        
    print(f"\nProcessing {filename}...")
    best_angle, results = get_best_rotation(img)
    print(f"Best rotation angle for {filename}: {best_angle} degrees")
    
    rotated = rotate_image(img, best_angle)
    cropped = crop_certificate_background(rotated)
    
    # Save output
    out_path = os.path.join(out_dir, filename)
    cv2.imwrite(out_path, cropped, [int(cv2.IMWRITE_JPEG_QUALITY), 92])
    print(f"Saved cropped upright image to {out_path} (shape: {cropped.shape})")
    
    # Extract readable text summary
    extracted_text = " ".join([res[1] for res in results if res[2] > 0.3])
    summary.append(f"{filename} | Angle: {best_angle} | Text: {extracted_text}")

with open(r'C:\Users\user\Desktop\arwad-portfolio\scratch\ocr_summary.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(summary))

print("\n--- Processing Finished! Summary written to ocr_summary.txt ---")
