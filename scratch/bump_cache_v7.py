import re

html_path = r'C:\Users\user\Desktop\arwad-portfolio\index.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update ?v=6 to ?v=7
updated_content = re.sub(r'assets/certificates/v2_IMG_0(6\d\d)\.jpg(\?v=\d+)?', r'assets/certificates/v2_IMG_0\1.jpg?v=7', content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(updated_content)

print("Updated index.html cache-busting version to v7!")
