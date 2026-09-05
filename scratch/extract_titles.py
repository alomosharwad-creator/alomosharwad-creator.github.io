import os
import cv2
import easyocr

reader = easyocr.Reader(['en', 'ar'], gpu=False, verbose=False)
out_dir = r'C:\Users\user\Desktop\arwad-portfolio\assets\certificates'
scratch_dir = r'C:\Users\user\Desktop\arwad-portfolio\scratch'
os.makedirs(scratch_dir, exist_ok=True)

files = sorted([f for f in os.listdir(out_dir) if f.endswith('.jpg')])

report = []

for f in files:
    filepath = os.path.join(out_dir, f)
    img = cv2.imread(filepath)
    if img is None:
        continue
    h, w = img.shape[:2]
    
    scale = 1000 / max(h, w)
    small = cv2.resize(img, (int(w * scale), int(h * scale)))
    
    ocr_res = reader.readtext(small)
    lines = [item[1] for item in ocr_res if item[2] > 0.2]
    
    full_text = " | ".join(lines)
    report.append(f"=== {f} ===\n{full_text}\n")
    print(f"Extracted {f}: {len(lines)} text elements")

with open(os.path.join(scratch_dir, "certificate_titles_ocr.txt"), "w", encoding="utf-8") as file_out:
    file_out.write("\n".join(report))

print("Saved OCR report to scratch/certificate_titles_ocr.txt")
