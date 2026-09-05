import http.server
import socketserver
import json
import os
import cv2
import subprocess

PORT = 8080
REPO_DIR = r'C:\Users\user\Desktop\arwad-portfolio'
RAW_DIR = r'C:\Users\user\Desktop\arwad-certificates\jpg'
CERT_DIR = r'C:\Users\user\Desktop\arwad-portfolio\assets\certificates'

class CertEditorHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Serve files from REPO_DIR
        rel_path = path.lstrip('/')
        if '?' in rel_path:
            rel_path = rel_path.split('?')[0]
        full_path = os.path.join(REPO_DIR, rel_path)
        if os.path.isdir(full_path):
            return os.path.join(full_path, 'index.html')
        return full_path

    def do_POST(self):
        if self.path == '/api/save_all':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            configs = json.loads(post_data.decode('utf-8'))
            
            print(f"\nReceived save request for {len(configs)} certificates...")
            
            # Process each certificate image on disk
            for img_name, cfg in configs.items():
                clean_name = img_name.replace('v2_', '').split('?')[0]
                raw_path = os.path.join(RAW_DIR, clean_name)
                out_path = os.path.join(CERT_DIR, clean_name)
                v2_path = os.path.join(CERT_DIR, f"v2_{clean_name}")
                
                # Load image from raw or current assets
                if os.path.exists(raw_path):
                    img = cv2.imread(raw_path)
                elif os.path.exists(out_path):
                    img = cv2.imread(out_path)
                else:
                    continue
                    
                if img is None:
                    continue
                    
                h, w = img.shape[:2]
                
                # 1. Apply rotation
                rot_angle = cfg.get('rot', 0) % 360
                if rot_angle == 90:
                    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
                elif rot_angle == 180:
                    img = cv2.rotate(img, cv2.ROTATE_180)
                elif rot_angle == 270:
                    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
                    
                ch, cw = img.shape[:2]
                
                # 2. Apply 4-side crop percentage
                top_pct = cfg.get('top', 0) / 100.0
                bot_pct = cfg.get('bottom', 0) / 100.0
                left_pct = cfg.get('left', 0) / 100.0
                right_pct = cfg.get('right', 0) / 100.0
                
                x1 = int(cw * left_pct)
                y1 = int(ch * top_pct)
                x2 = int(cw * (1.0 - right_pct))
                y2 = int(ch * (1.0 - bot_pct))
                
                x1 = max(0, min(cw - 10, x1))
                y1 = max(0, min(ch - 10, y1))
                x2 = max(x1 + 10, min(cw, x2))
                y2 = max(y1 + 10, min(ch, y2))
                
                cropped = img[y1:y2, x1:x2]
                
                # Save processed cropped image
                cv2.imwrite(out_path, cropped, [int(cv2.IMWRITE_JPEG_QUALITY), 93])
                cv2.imwrite(v2_path, cropped, [int(cv2.IMWRITE_JPEG_QUALITY), 93])
                print(f"Processed & Saved {clean_name}: size {cropped.shape[1]}x{cropped.shape[0]}")
                
            # Run Git Commit and Push to GitHub Pages
            try:
                subprocess.run(['git', 'add', 'assets/certificates/*'], cwd=REPO_DIR, check=True)
                subprocess.run(['git', 'commit', '-m', 'fix: apply manual certificate edits & crops to repository'], cwd=REPO_DIR, check=True)
                subprocess.run(['git', 'push', 'origin', 'main'], cwd=REPO_DIR, check=True)
                push_status = "Successfully updated repository & pushed live to GitHub Pages!"
            except Exception as git_err:
                push_status = f"Saved to disk locally, Git push note: {git_err}"
                
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {"success": True, "message": push_status}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            super().do_POST()

print(f"Starting Certificate Studio Server on http://localhost:{PORT}...")
with socketserver.TCPServer(("", PORT), CertEditorHandler) as httpd:
    httpd.serve_forever()
