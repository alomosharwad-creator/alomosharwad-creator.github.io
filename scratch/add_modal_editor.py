import re

html_path = r'C:\Users\user\Desktop\arwad-portfolio\index.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace credential-modal structure with interactive rotation & crop editor modal
old_modal_pattern = r'<!-- Lightbox Modal for Credential Viewer -->.*?</script>'

new_modal_html = '''<!-- Lightbox Modal for Credential Viewer with Interactive Rotate & Crop Tools -->
        <div id="credential-modal" class="fixed inset-0 z-50 hidden bg-black/85 backdrop-blur-md flex items-center justify-center p-3 sm:p-6 select-none">
            <div class="relative bg-white rounded-2xl max-w-5xl w-full max-h-[92vh] overflow-hidden shadow-2xl flex flex-col border border-gray-100">
                <!-- Modal Header -->
                <div class="p-4 border-b border-gray-100 flex items-center justify-between bg-gray-50/90">
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-indigo-50 text-indigo-700 border border-indigo-100 font-mono">INTERACTIVE EDITOR</span>
                            <h3 id="modal-title" class="text-base font-semibold text-gray-900 leading-snug">Credential Viewer</h3>
                        </div>
                        <p id="modal-issuer" class="text-xs text-gray-500 font-mono mt-0.5"></p>
                    </div>
                    <button onclick="closeCredentialModal()" class="p-2 text-gray-400 hover:text-gray-900 rounded-full hover:bg-gray-200 transition">
                        <i data-lucide="x" class="w-5 h-5"></i>
                    </button>
                </div>

                <!-- Interactive Edit Toolbar -->
                <div class="bg-gray-900 text-white px-4 py-3 flex flex-wrap items-center justify-between gap-3 text-xs border-b border-gray-800">
                    <div class="flex flex-wrap items-center gap-2">
                        <span class="text-gray-400 font-mono text-[11px] mr-1">TOOLS:</span>
                        
                        <button onclick="rotateModalImg(-90)" class="px-3 py-1.5 bg-gray-800 hover:bg-gray-700 text-gray-200 rounded-lg transition flex items-center gap-1.5 border border-gray-700">
                            <i data-lucide="rotate-ccw" class="w-3.5 h-3.5 text-indigo-400"></i>
                            <span>Rotate -90°</span>
                        </button>
                        
                        <button onclick="rotateModalImg(90)" class="px-3 py-1.5 bg-gray-800 hover:bg-gray-700 text-gray-200 rounded-lg transition flex items-center gap-1.5 border border-gray-700">
                            <i data-lucide="rotate-cw" class="w-3.5 h-3.5 text-indigo-400"></i>
                            <span>Rotate +90°</span>
                        </button>
                        
                        <button onclick="rotateModalImg(180)" class="px-3 py-1.5 bg-gray-800 hover:bg-gray-700 text-gray-200 rounded-lg transition flex items-center gap-1.5 border border-gray-700">
                            <i data-lucide="refresh-cw" class="w-3.5 h-3.5 text-indigo-400"></i>
                            <span>Flip 180°</span>
                        </button>

                        <div class="h-4 w-px bg-gray-700 mx-1 hidden sm:block"></div>

                        <button onclick="adjustModalCrop(0.05)" class="px-3 py-1.5 bg-gray-800 hover:bg-gray-700 text-gray-200 rounded-lg transition flex items-center gap-1.5 border border-gray-700">
                            <i data-lucide="zoom-in" class="w-3.5 h-3.5 text-emerald-400"></i>
                            <span>Crop In (+5%)</span>
                        </button>

                        <button onclick="adjustModalCrop(-0.05)" class="px-3 py-1.5 bg-gray-800 hover:bg-gray-700 text-gray-200 rounded-lg transition flex items-center gap-1.5 border border-gray-700">
                            <i data-lucide="zoom-out" class="w-3.5 h-3.5 text-emerald-400"></i>
                            <span>Crop Out (-5%)</span>
                        </button>

                        <button onclick="resetModalImg()" class="px-2.5 py-1.5 bg-gray-800 hover:bg-gray-700 text-gray-400 hover:text-white rounded-lg transition border border-gray-700">
                            <span>Reset</span>
                        </button>
                    </div>

                    <div class="flex items-center gap-2">
                        <span id="editor-status" class="text-[11px] font-mono text-gray-400 bg-gray-950 px-2.5 py-1 rounded-md border border-gray-800">Rot: 0° | Crop: 100%</span>
                        <button onclick="downloadEditedModalImg()" class="px-3.5 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white font-medium rounded-lg transition flex items-center gap-1.5 shadow-sm">
                            <i data-lucide="download" class="w-3.5 h-3.5"></i>
                            <span>Download Edited Image</span>
                        </button>
                    </div>
                </div>

                <!-- Viewer Workspace -->
                <div class="p-6 overflow-hidden flex items-center justify-center bg-gray-950 min-h-[420px] max-h-[70vh] relative">
                    <div id="modal-img-container" class="relative overflow-hidden flex items-center justify-center transition-all duration-300">
                        <img id="modal-img" src="" alt="Credential" class="max-h-[65vh] w-auto object-contain transition-transform duration-300 shadow-xl rounded-sm">
                    </div>
                </div>

                <!-- Footer -->
                <div class="p-3.5 border-t border-gray-100 bg-gray-50 flex items-center justify-between text-xs text-gray-500">
                    <span class="font-mono text-gray-400">MANUAL ROTATION & CROP EDITOR ENABLED</span>
                    <button onclick="closeCredentialModal()" class="px-4 py-1.5 bg-gray-900 text-white font-medium rounded-full hover:bg-black transition">Close Viewer</button>
                </div>
            </div>
        </div>

        <script>
            let currentRotation = 0;
            let currentScale = 1.0;
            let currentImgSrc = '';

            function filterCredentials(category) {
                const cards = document.querySelectorAll('.cred-card');
                const filterBtns = document.querySelectorAll('.cred-filter-btn');

                filterBtns.forEach(btn => {
                    if (btn.getAttribute('data-filter') === category) {
                        btn.classList.add('bg-gray-900', 'text-white');
                        btn.classList.remove('bg-white', 'text-gray-700', 'border-gray-200');
                    } else {
                        btn.classList.remove('bg-gray-900', 'text-white');
                        btn.classList.add('bg-white', 'text-gray-700', 'border-gray-200');
                    }
                });

                cards.forEach(card => {
                    if (category === 'all' || card.getAttribute('data-category') === category) {
                        card.style.display = 'flex';
                    } else {
                        card.style.display = 'none';
                    }
                });
            }

            function openCredentialModal(imgSrc, title, issuer) {
                currentImgSrc = imgSrc;
                currentRotation = 0;
                currentScale = 1.0;
                
                const imgEl = document.getElementById('modal-img');
                imgEl.src = imgSrc;
                imgEl.style.transform = `rotate(${currentRotation}deg) scale(${currentScale})`;
                
                document.getElementById('modal-title').textContent = title;
                document.getElementById('modal-issuer').textContent = issuer;
                updateEditorStatus();
                
                document.getElementById('credential-modal').classList.remove('hidden');
                document.body.style.overflow = 'hidden';
                if (window.lucide) lucide.createIcons();
            }

            function closeCredentialModal() {
                document.getElementById('credential-modal').classList.add('hidden');
                document.body.style.overflow = 'auto';
            }

            function rotateModalImg(degrees) {
                currentRotation = (currentRotation + degrees) % 360;
                if (currentRotation < 0) currentRotation += 360;
                applyTransform();
            }

            function adjustModalCrop(delta) {
                currentScale = Math.max(0.8, Math.min(2.5, currentScale + delta));
                applyTransform();
            }

            function resetModalImg() {
                currentRotation = 0;
                currentScale = 1.0;
                applyTransform();
            }

            function applyTransform() {
                const imgEl = document.getElementById('modal-img');
                imgEl.style.transform = `rotate(${currentRotation}deg) scale(${currentScale})`;
                updateEditorStatus();
            }

            function updateEditorStatus() {
                const cropPct = Math.round(currentScale * 100);
                document.getElementById('editor-status').textContent = `Rot: ${currentRotation}° | Crop: ${cropPct}%`;
            }

            function downloadEditedModalImg() {
                const imgEl = document.getElementById('modal-img');
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                
                const tempImg = new Image();
                tempImg.crossOrigin = 'anonymous';
                tempImg.onload = function() {
                    const iw = tempImg.naturalWidth;
                    const ih = tempImg.naturalHeight;
                    
                    const rad = currentRotation * Math.PI / 180;
                    const sin = Math.abs(Math.sin(rad));
                    const cos = Math.abs(Math.cos(rad));
                    
                    const rotatedW = Math.floor(iw * cos + ih * sin);
                    const rotatedH = Math.floor(iw * sin + ih * cos);
                    
                    canvas.width = rotatedW;
                    canvas.height = rotatedH;
                    
                    ctx.translate(rotatedW / 2, rotatedH / 2);
                    ctx.rotate(rad);
                    ctx.drawImage(tempImg, -iw / 2, -ih / 2);
                    
                    // If scaled/cropped, crop inner canvas box
                    if (currentScale > 1.0) {
                        const cropCanvas = document.createElement('canvas');
                        const cropCtx = cropCanvas.getContext('2d');
                        
                        const cropW = Math.floor(rotatedW / currentScale);
                        const cropH = Math.floor(rotatedH / currentScale);
                        const cropX = Math.floor((rotatedW - cropW) / 2);
                        const cropY = Math.floor((rotatedH - cropH) / 2);
                        
                        cropCanvas.width = cropW;
                        cropCanvas.height = cropH;
                        
                        cropCtx.drawImage(canvas, cropX, cropY, cropW, cropH, 0, 0, cropW, cropH);
                        
                        const link = document.createElement('a');
                        link.download = `edited_${currentImgSrc.split('/').pop()}`;
                        link.href = cropCanvas.toDataURL('image/jpeg', 0.95);
                        link.click();
                    } else {
                        const link = document.createElement('a');
                        link.download = `edited_${currentImgSrc.split('/').pop()}`;
                        link.href = canvas.toDataURL('image/jpeg', 0.95);
                        link.click();
                    }
                };
                tempImg.src = currentImgSrc;
            }

            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape') {
                    closeCredentialModal();
                }
            });
        </script>'''

updated_html = re.sub(old_modal_pattern, new_modal_html, content, flags=re.DOTALL)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(updated_html)

print("Successfully injected Interactive Rotate & Crop Editor Modal into index.html!")
