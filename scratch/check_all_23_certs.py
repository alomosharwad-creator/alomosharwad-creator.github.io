import os
import cv2
import easyocr

reader = easyocr.Reader(['en', 'ar'], gpu=False, verbose=False)
out_dir = r'C:\Users\user\Desktop\arwad-portfolio\assets\certificates'

# We can test multiple angles (0, 90, 180, 270) specifically for any remaining image that might be sideways
files = sorted([f for f in os.listdir(out_dir) if f.endswith('.jpg')])

cert_details = {}

for f in files:
    filepath = os.path.join(out_dir, f)
    img = cv2.imread(filepath)
    if img is None:
        continue
    h, w = img.shape[:2]
    
    # Check if height > width or width > height
    # Let's test 4 angles to find the absolute best English/Arabic readable text
    best_text = ""
    best_angle = 0
    max_len = -1
    
    scale = 800 / max(h, w)
    small = cv2.resize(img, (int(w * scale), int(h * scale)))
    
    for angle in [0, 90, 180, 270]:
        if angle == 90:
            rot = cv2.rotate(small, cv2.ROTATE_90_CLOCKWISE)
        elif angle == 180:
            rot = cv2.rotate(small, cv2.ROTATE_180)
        elif angle == 270:
            rot = cv2.rotate(small, cv2.ROTATE_90_COUNTERCLOCKWISE)
        else:
            rot = small
            
        ocr = reader.readtext(rot)
        txts = [it[1] for it in ocr if it[2] > 0.2]
        combined = " | ".join(txts)
        
        # Check count of valid English words
        valid_words = sum(1 for w in combined.split() if len(w) > 2)
        if valid_words > max_len:
            max_len = valid_words
            best_angle = angle
            best_text = combined
            
    # If a rotation was better than current image, re-rotate and re-crop!
    if best_angle != 0:
        if best_angle == 90:
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        elif best_angle == 180:
            img = cv2.rotate(img, cv2.ROTATE_180)
        elif best_angle == 270:
            img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        cv2.imwrite(filepath, img, [int(cv2.IMWRITE_JPEG_QUALITY), 92])
        print(f"Re-rotated {f} by additional {best_angle}° to ensure upright text")
        
    cert_details[f] = best_text
    print(f"Final {f} (shape {img.shape[:2]}): {best_text[:120]}")

with open(r'C:\Users\user\Desktop\arwad-portfolio\scratch\final_cert_ocr.txt', 'w', encoding='utf-8') as out:
    for k, v in cert_details.items():
        out.write(f"{k}: {v}\n")
