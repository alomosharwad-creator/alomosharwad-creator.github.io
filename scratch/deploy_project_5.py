import os
import shutil

src_dir = r'C:\Users\user\Desktop\aegistwin-vision'
dest_dir = r'C:\Users\user\Desktop\arwad-portfolio\projects\aegistwin-vision'

if os.path.exists(dest_dir):
    shutil.rmtree(dest_dir)

# Copy all files except .git
def ignore_git(dir, files):
    return ['.git']

shutil.copytree(src_dir, dest_dir, ignore=ignore_git)
print("Successfully copied aegistwin-vision into portfolio projects directory!")
