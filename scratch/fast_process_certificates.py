import os
import cv2
import numpy as np
import easyocr

print("Initializing EasyOCR reader...")
reader = easyocr.Reader(['en'], gpu=False, verbose=False)

raw_dir = r'C:\Users\user\Desktop\arwad-certificates\jpg'
out_dir = r'C:\Users\user\Desktop\arwad-portfolio\assets\certificates'
os.makedirs(out_dir, exist_ok=True)

files = sorted([f for f in os.listdir(raw_dir) if f.endswith('.jpg')])

keywords = [
    "certificate", "appreciation", "participation", "attendance", "awarded", "present",
    "ieee", "google", "arwad", "alomosh", "university", "completion", "contest",
    "workshop", "leadership", "event", "robot", "sumo", "course", "training", "honor",
    "jora", "shai", "htu", "al-balqa", "bau", "hashemite", "jordan", "aess", "wie"
]

def rotate_image(img, angle):
    if angle == 90:
        return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    elif angle == 180:
        return cv2.rotate(img, cv2.ROTATE_180)
    elif angle == 270:
        return cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return img

def crop_certificate_paper(img):
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Gaussian blur
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    
    # Adaptive / Canny edges or Otsu thresh
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Morphological closing to fill holes in certificate paper
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    img_area = h * w
    best_rect = None
    max_area = 0
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 0.20 * img_area:
            x, y, bw, bh = cv2.boundingRect(cnt)
            # Ensure it looks like a certificate bounding rectangle (not tiny)
            if area > max_area:
                max_area = area
                best_rect = (x, y, bw, bh)
                
    if best_rect is not None:
        x, y, bw, bh = best_rect
        # Safety crop margins: slight inner crop to eliminate desk/table edges completely
        margin_x = int(bw * 0.015)
        margin_y = int(bh * 0.015)
        
        x1 = max(0, x + margin_x)
        y1 = max(0, y + margin_y)
        x2 = min(w, x + bw - margin_x)
        y2 = min(h, y + bh - margin_y)
        
        if (x2 - x1) > 0.3 * w and (y2 - y1) > 0.3 * h:
            return img[y1:y2, x1:x2]
            
    # Fallback smart crop (4% inner crop)
    pad_h = int(h * 0.04)
    pad_w = int(w * 0.04)
    return img[pad_h:h-pad_h, pad_w:w-pad_w]

results_data = []

for filename in files:
    filepath = os.path.join(raw_dir, filename)
    img = cv2.imread(filepath)
    if img is None:
        continue
        
    h, w = img.shape[:2]
    # Fast thumbnail for orientation test
    thumb = cv2.resize(img, (400, int(400 * h / w))) if w > h else cv2.resize(img, (int(400 * w / h), 400))
    
    best_angle = 0
    max_score = -1
    best_text_list = []
    
    for angle in [0, 90, 180, 270]:
        rot_thumb = rotate_image(thumb, angle)
        ocr_res = reader.readtext(rot_thumb)
        
        score = 0
        texts = []
        for bbox, text, prob in ocr_res:
            if prob > 0.2:
                texts.append(text)
                score += len(text) * prob
                t_lower = text.lower()
                for kw in keywords:
                    if kw in t_lower:
                        score += 40 * prob
                        
        if score > max_score:
            max_score = score
            best_angle = angle
            best_text_list = texts
            
    print(f"[{filename}] Best Angle: {best_angle} | OCR Score: {max_score:.1f}")
    
    # Rotate full res image
    full_rotated = rotate_image(img, best_angle)
    
    # Crop certificate paper background
    cropped_img = crop_certificate_paper(full_rotated)
    
    # Save output image
    out_path = os.path.join(out_dir, filename)
    cv2.imwrite(out_path, cropped_img, [int(cv2.IMWRITE_JPEG_QUALITY), 92])
    
    # One more OCR pass on cropped upright image to get full text summary
    ocr_crop_thumb = cv2.resize(cropped_img, (800, int(800 * cropped_img.shape[0] / cropped_img.shape[1])))
    full_ocr = reader.readtext(ocr_crop_thumb)
    full_text = " | ".join([item[1] for item in full_ocr if item[2] > 0.25])
    
    results_data.append(f"### {filename}\n- **Rotation Angle**: {best_angle}°\n- **Extracted Text**: {full_text}\n")

summary_path = r'C:\Users\user\Desktop\arwad-portfolio\scratch\certificate_extracted_data.md'
with open(summary_path, 'w', encoding='utf-8') as f:
    f.write("\n".join(results_data))

print(f"\nCompleted! Saved all 23 cropped certificates to {out_dir}")
print(f"Detailed OCR metadata saved to {summary_path}")
