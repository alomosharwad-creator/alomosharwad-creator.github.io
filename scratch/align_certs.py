import os
import cv2
import easyocr

reader = easyocr.Reader(['en', 'ar'], gpu=False, verbose=False)
out_dir = r'C:\Users\user\Desktop\arwad-portfolio\assets\certificates'
files = sorted([f for f in os.listdir(out_dir) if f.endswith('.jpg')])

keywords = [
    "certificate", "appreciation", "participation", "attendance", "awarded", "present",
    "ieee", "google", "arwad", "alomosh", "university", "completion", "contest",
    "workshop", "leadership", "event", "robot", "sumo", "course", "training", "honor",
    "jora", "shai", "htu", "al-balqa", "bau", "hashemite", "jordan", "aess", "wie", "devfest"
]

print("Checking final orientation for all 23 certificates...")

for f in files:
    filepath = os.path.join(out_dir, f)
    img = cv2.imread(filepath)
    if img is None:
        continue
        
    best_img = img
    max_score = -1
    best_angle = 0
    
    h, w = img.shape[:2]
    
    # Test 4 angles (0, 90, 180, 270)
    for angle in [0, 90, 180, 270]:
        if angle == 90:
            candidate = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        elif angle == 180:
            candidate = cv2.rotate(img, cv2.ROTATE_180)
        elif angle == 270:
            candidate = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        else:
            candidate = img
            
        ch, cw = candidate.shape[:2]
        
        # We prefer landscape for standard certificates (width > height)
        aspect_bonus = 25.0 if cw > ch else 0.0
        
        # Resize thumbnail for OCR evaluation
        scale = 500 / max(ch, cw)
        thumb = cv2.resize(candidate, (int(cw * scale), int(ch * scale)))
        
        ocr_res = reader.readtext(thumb)
        score = aspect_bonus
        for bbox, text, prob in ocr_res:
            if prob > 0.2:
                score += len(text) * prob
                t_lower = text.lower()
                for kw in keywords:
                    if kw in t_lower:
                        score += 35 * prob
                        
        if score > max_score:
            max_score = score
            best_img = candidate
            best_angle = angle
            
    cv2.imwrite(filepath, best_img, [int(cv2.IMWRITE_JPEG_QUALITY), 92])
    final_h, final_w = best_img.shape[:2]
    print(f"[{f}] Final size: {final_w}x{final_h} | Rotated: {best_angle}° | OCR Score: {max_score:.1f}")

print("\nAll 23 certificate images have been aligned upright & saved!")
