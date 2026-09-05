import os
import cv2
import shutil
import re

cert_dir = r'C:\Users\user\Desktop\arwad-portfolio\assets\certificates'
html_path = r'C:\Users\user\Desktop\arwad-portfolio\index.html'

def ultra_tight_crop(img):
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Gaussian blur & Otsu threshold
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    img_area = h * w
    
    best_rect = None
    max_area = 0
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 0.15 * img_area:
            bx, by, bw, bh = cv2.boundingRect(cnt)
            if area > max_area:
                max_area = area
                best_rect = (bx, by, bw, bh)
                
    if best_rect is not None:
        bx, by, bw, bh = best_rect
        margin_x = int(bw * 0.02)
        margin_y = int(bh * 0.02)
        
        x1 = max(0, bx + margin_x)
        y1 = max(0, by + margin_y)
        x2 = min(w, bx + bw - margin_x)
        y2 = min(h, by + bh - margin_y)
        
        if (x2 - x1) > 0.3 * w and (y2 - y1) > 0.3 * h:
            return img[y1:y2, x1:x2]
            
    pad_h = int(h * 0.05)
    pad_w = int(w * 0.05)
    return img[pad_h:h-pad_h, pad_w:w-pad_w]

print("Applying ultra-tight crop to all updated images...")

for i in range(673, 696):
    img_name = f"IMG_0{i}.jpg"
    v2_name = f"v2_IMG_0{i}.jpg"
    
    img_path = os.path.join(cert_dir, img_name)
    v2_path = os.path.join(cert_dir, v2_name)
    
    if os.path.exists(img_path):
        img = cv2.imread(img_path)
        cropped = ultra_tight_crop(img)
        cv2.imwrite(img_path, cropped, [int(cv2.IMWRITE_JPEG_QUALITY), 93])
        cv2.imwrite(v2_path, cropped, [int(cv2.IMWRITE_JPEG_QUALITY), 93])
        print(f"Processed & synchronized {v2_name}: {cropped.shape[1]}x{cropped.shape[0]}")

# Update index.html to ?v=4
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

updated_content = re.sub(r'assets/certificates/v2_IMG_0(6\d\d)\.jpg(\?v=\d+)?', r'assets/certificates/v2_IMG_0\1.jpg?v=4', content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(updated_content)

print("Updated index.html cache version to v4!")
