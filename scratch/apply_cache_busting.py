import os
import shutil
import re

cert_dir = r'C:\Users\user\Desktop\arwad-portfolio\assets\certificates'
html_path = r'C:\Users\user\Desktop\arwad-portfolio\index.html'

# 1. Create v2 copies of all 23 certificate images
for i in range(673, 696):
    old_name = f"IMG_0{i}.jpg"
    v2_name = f"v2_IMG_0{i}.jpg"
    old_path = os.path.join(cert_dir, old_name)
    v2_path = os.path.join(cert_dir, v2_name)
    if os.path.exists(old_path):
        shutil.copy2(old_path, v2_path)
        print(f"Created cache-busted copy: {v2_name}")

# 2. Update index.html to point to v2_IMG_0xxx.jpg?v=2
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Replace references like 'assets/certificates/IMG_0673.jpg' with 'assets/certificates/v2_IMG_0673.jpg?v=2'
updated_html = re.sub(r'assets/certificates/IMG_0(6\d\d)\.jpg', r'assets/certificates/v2_IMG_0\1.jpg?v=2', html_content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(updated_html)

print("Updated index.html with cache-busted image URLs!")
