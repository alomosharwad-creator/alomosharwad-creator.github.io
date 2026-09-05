import os
import cv2
import numpy as np

raw_dir = r'C:\Users\user\Desktop\arwad-certificates\jpg'
cert_dir = r'C:\Users\user\Desktop\arwad-portfolio\assets\certificates'
scratch_dir = r'C:\Users\user\Desktop\arwad-portfolio\scratch'

files = sorted([f for f in os.listdir(cert_dir) if f.startswith('v2_IMG_') and f.endswith('.jpg')])

def rotate_image(img, angle):
    if angle == 90:
        return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    elif angle == 180:
        return cv2.rotate(img, cv2.ROTATE_180)
    elif angle == 270:
        return cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return img

def ultra_tight_crop(img):
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 1. Edge-based crop and color variance crop
    # Sample corner pixels to detect desk/table color (e.g. brown wood or dark mat)
    corner_samples = np.vstack([
        img[:20, :20].reshape(-1, 3),
        img[:20, -20:].reshape(-1, 3),
        img[-20:, :20].reshape(-1, 3),
        img[-20:, -20:].reshape(-1, 3)
    ])
    bg_color = np.median(corner_samples, axis=0)
    
    # Compute distance from background color
    diff = np.linalg.norm(img.astype(float) - bg_color, axis=2)
    
    # Mask where pixel differs significantly from background color (paper/badge)
    fg_mask = (diff > 30).astype(uint8 if 'uint8' in str(type(diff)) else np.uint8) * 255
    
    # Also combine with brightness threshold (paper is usually bright)
    _, bright_mask = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY)
    
    combined_mask = cv2.bitwise_or(fg_mask, bright_mask)
    
    # Morphological closing
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
    closed = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel)
    
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    best_rect = None
    max_area = 0
    img_area = h * w
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 0.15 * img_area:
            bx, by, bw, bh = cv2.boundingRect(cnt)
            if area > max_area:
                max_area = area
                best_rect = (bx, by, bw, bh)
                
    if best_rect is not None:
        bx, by, bw, bh = best_rect
        # Tight crop: trim 1.5% inside bounding rect to ensure 0% table pixels remain
        trim_w = int(bw * 0.02)
        trim_h = int(bh * 0.02)
        
        x1 = max(0, bx + trim_w)
        y1 = max(0, by + trim_h)
        x2 = min(w, bx + bw - trim_w)
        y2 = min(h, by + bh - trim_h)
        
        if (x2 - x1) > 0.3 * w and (y2 - y1) > 0.3 * h:
            return img[y1:y2, x1:x2]
            
    # Fallback: aggressive 6% crop from all 4 borders
    pad_h = int(h * 0.06)
    pad_w = int(w * 0.06)
    return img[pad_h:h-pad_h, pad_w:w-pad_w]

print("Performing ultra-tight crop on all 23 certificates & badges...")

for filename in files:
    filepath = os.path.join(cert_dir, filename)
    img = cv2.imread(filepath)
    if img is None:
        continue
        
    orig_h, orig_w = img.shape[:2]
    tight = ultra_tight_crop(img)
    tight_h, tight_w = tight.shape[:2]
    
    # Save back to v2_IMG_... and IMG_...
    cv2.imwrite(filepath, tight, [int(cv2.IMWRITE_JPEG_QUALITY), 93])
    
    base_name = filename.replace('v2_', '')
    base_path = os.path.join(cert_dir, base_name)
    cv2.imwrite(base_path, tight, [int(cv2.IMWRITE_JPEG_QUALITY), 93])
    
    print(f"[{filename}] Cropped from {orig_w}x{orig_h} -> {tight_w}x{tight_h}")

print("\nUltra-tight crop completed!")
