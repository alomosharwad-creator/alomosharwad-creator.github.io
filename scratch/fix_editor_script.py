import re

html_path = r'C:\Users\user\Desktop\arwad-portfolio\index.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the modal script with a bulletproof, optimized version
old_script_pattern = r'<!-- Lightbox Modal for Credential Viewer with 4-Side Crop & Save Tools -->.*?</script>'

new_script_code = '''<!-- Lightbox Modal for Credential Viewer with 4-Side Crop & Save Tools -->
        <div id="credential-modal" class="fixed inset-0 z-50 hidden bg-black/85 backdrop-blur-md flex items-center justify-center p-2 sm:p-4 select-none">
            <div class="relative bg-white rounded-2xl max-w-5xl w-full max-h-[95vh] overflow-hidden shadow-2xl flex flex-col border border-gray-100">
                
                <!-- Modal Header -->
                <div class="p-3 sm:p-4 border-b border-gray-100 flex items-center justify-between bg-gray-50/90">
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-indigo-50 text-indigo-700 border border-indigo-100 font-mono">LIVE 4-EDGE CROPPER</span>
                            <h3 id="modal-title" class="text-base font-semibold text-gray-900 leading-snug">Credential Editor</h3>
                        </div>
                        <p id="modal-issuer" class="text-xs text-gray-500 font-mono mt-0.5"></p>
                    </div>
                    <div class="flex items-center gap-2">
                        <button onclick="saveAndApplyModalImg()" class="px-4 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold rounded-lg transition flex items-center gap-1.5 shadow-sm">
                            <i data-lucide="check-circle" class="w-3.5 h-3.5"></i>
                            <span>Save & Apply Changes</span>
                        </button>
                        <button onclick="closeCredentialModal()" class="p-2 text-gray-400 hover:text-gray-900 rounded-full hover:bg-gray-200 transition">
                            <i data-lucide="x" class="w-5 h-5"></i>
                        </button>
                    </div>
                </div>

                <!-- Interactive Rotation & 4-Side Edge Trimming Toolbar -->
                <div class="bg-gray-900 text-white p-3 sm:p-4 flex flex-col gap-3 text-xs border-b border-gray-800">
                    
                    <!-- Row 1: Rotation Tools & Actions -->
                    <div class="flex flex-wrap items-center justify-between gap-2 border-b border-gray-800/80 pb-2.5">
                        <div class="flex flex-wrap items-center gap-2">
                            <span class="text-gray-400 font-mono text-[11px] mr-1">ROTATE:</span>
                            <button onclick="rotateModalImg(-90)" class="px-2.5 py-1 bg-gray-800 hover:bg-gray-700 text-gray-200 rounded-md transition flex items-center gap-1 border border-gray-700">
                                <i data-lucide="rotate-ccw" class="w-3.5 h-3.5 text-indigo-400"></i>
                                <span>-90°</span>
                            </button>
                            <button onclick="rotateModalImg(90)" class="px-2.5 py-1 bg-gray-800 hover:bg-gray-700 text-gray-200 rounded-md transition flex items-center gap-1 border border-gray-700">
                                <i data-lucide="rotate-cw" class="w-3.5 h-3.5 text-indigo-400"></i>
                                <span>+90°</span>
                            </button>
                            <button onclick="rotateModalImg(180)" class="px-2.5 py-1 bg-gray-800 hover:bg-gray-700 text-gray-200 rounded-md transition flex items-center gap-1 border border-gray-700">
                                <i data-lucide="refresh-cw" class="w-3.5 h-3.5 text-indigo-400"></i>
                                <span>180°</span>
                            </button>
                            <button onclick="resetModalImg()" class="px-2.5 py-1 bg-gray-800 hover:bg-gray-700 text-gray-400 hover:text-white rounded-md transition border border-gray-700 ml-1">
                                <span>Reset All</span>
                            </button>
                        </div>

                        <div class="flex items-center gap-2">
                            <span id="editor-status" class="text-[11px] font-mono text-gray-400 bg-gray-950 px-2.5 py-1 rounded-md border border-gray-800">Rot: 0° | Inset: T0% R0% B0% L0%</span>
                            <button onclick="downloadEditedModalImg()" class="px-3 py-1 bg-gray-800 hover:bg-gray-700 text-gray-200 text-xs font-medium rounded-md transition flex items-center gap-1.5 border border-gray-700">
                                <i data-lucide="download" class="w-3.5 h-3.5 text-indigo-400"></i>
                                <span>Download File</span>
                            </button>
                        </div>
                    </div>

                    <!-- Row 2: 4-Side Edge Crop Sliders -->
                    <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 items-center">
                        <div class="flex flex-col gap-1">
                            <div class="flex justify-between text-[11px] text-gray-400 font-mono">
                                <span>Crop Top</span>
                                <span id="val-top">0%</span>
                            </div>
                            <input type="range" id="crop-top" min="0" max="35" value="0" step="0.5" oninput="update4SideCrop()" class="accent-indigo-500 cursor-pointer h-1.5 bg-gray-800 rounded-lg">
                        </div>

                        <div class="flex flex-col gap-1">
                            <div class="flex justify-between text-[11px] text-gray-400 font-mono">
                                <span>Crop Bottom</span>
                                <span id="val-bottom">0%</span>
                            </div>
                            <input type="range" id="crop-bottom" min="0" max="35" value="0" step="0.5" oninput="update4SideCrop()" class="accent-indigo-500 cursor-pointer h-1.5 bg-gray-800 rounded-lg">
                        </div>

                        <div class="flex flex-col gap-1">
                            <div class="flex justify-between text-[11px] text-gray-400 font-mono">
                                <span>Crop Left</span>
                                <span id="val-left">0%</span>
                            </div>
                            <input type="range" id="crop-left" min="0" max="35" value="0" step="0.5" oninput="update4SideCrop()" class="accent-indigo-500 cursor-pointer h-1.5 bg-gray-800 rounded-lg">
                        </div>

                        <div class="flex flex-col gap-1">
                            <div class="flex justify-between text-[11px] text-gray-400 font-mono">
                                <span>Crop Right</span>
                                <span id="val-right">0%</span>
                            </div>
                            <input type="range" id="crop-right" min="0" max="35" value="0" step="0.5" oninput="update4SideCrop()" class="accent-indigo-500 cursor-pointer h-1.5 bg-gray-800 rounded-lg">
                        </div>
                    </div>

                </div>

                <!-- Viewer Workspace -->
                <div class="p-4 overflow-hidden flex items-center justify-center bg-gray-950 min-h-[380px] max-h-[65vh] relative">
                    <div id="modal-img-container" class="relative overflow-hidden flex items-center justify-center transition-all duration-300">
                        <img id="modal-img" src="" alt="Credential" class="max-h-[60vh] w-auto object-contain transition-all duration-150 shadow-xl rounded-sm">
                    </div>
                </div>

                <!-- Footer -->
                <div class="p-3 border-t border-gray-100 bg-gray-50 flex items-center justify-between text-xs text-gray-500">
                    <span class="font-mono text-gray-400">4-EDGE TRIMMING ENABLED // PERSISTENT SAVE READY</span>
                    <div class="flex items-center gap-2">
                        <button onclick="saveAndApplyModalImg()" class="px-4 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white font-medium rounded-full transition shadow-sm">Save & Apply</button>
                        <button onclick="closeCredentialModal()" class="px-4 py-1.5 bg-gray-900 text-white font-medium rounded-full hover:bg-black transition">Close</button>
                    </div>
                </div>
            </div>
        </div>

        <script>
            let currentRotation = 0;
            let currentCropTop = 0;
            let currentCropBottom = 0;
            let currentCropLeft = 0;
            let currentCropRight = 0;
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
                currentCropTop = 0;
                currentCropBottom = 0;
                currentCropLeft = 0;
                currentCropRight = 0;
                
                document.getElementById('crop-top').value = 0;
                document.getElementById('crop-bottom').value = 0;
                document.getElementById('crop-left').value = 0;
                document.getElementById('crop-right').value = 0;

                document.getElementById('val-top').textContent = '0%';
                document.getElementById('val-bottom').textContent = '0%';
                document.getElementById('val-left').textContent = '0%';
                document.getElementById('val-right').textContent = '0%';

                const imgEl = document.getElementById('modal-img');
                
                try {
                    const savedData = localStorage.getItem('saved_cert_' + imgSrc);
                    if (savedData) {
                        imgEl.src = savedData;
                    } else {
                        imgEl.src = imgSrc;
                    }
                } catch(e) {
                    imgEl.src = imgSrc;
                }

                document.getElementById('modal-title').textContent = title;
                document.getElementById('modal-issuer').textContent = issuer;
                
                applyTransform();
                
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

            function update4SideCrop() {
                currentCropTop = parseFloat(document.getElementById('crop-top').value) || 0;
                currentCropBottom = parseFloat(document.getElementById('crop-bottom').value) || 0;
                currentCropLeft = parseFloat(document.getElementById('crop-left').value) || 0;
                currentCropRight = parseFloat(document.getElementById('crop-right').value) || 0;

                document.getElementById('val-top').textContent = currentCropTop + '%';
                document.getElementById('val-bottom').textContent = currentCropBottom + '%';
                document.getElementById('val-left').textContent = currentCropLeft + '%';
                document.getElementById('val-right').textContent = currentCropRight + '%';

                applyTransform();
            }

            function resetModalImg() {
                currentRotation = 0;
                currentCropTop = 0;
                currentCropBottom = 0;
                currentCropLeft = 0;
                currentCropRight = 0;

                document.getElementById('crop-top').value = 0;
                document.getElementById('crop-bottom').value = 0;
                document.getElementById('crop-left').value = 0;
                document.getElementById('crop-right').value = 0;

                document.getElementById('val-top').textContent = '0%';
                document.getElementById('val-bottom').textContent = '0%';
                document.getElementById('val-left').textContent = '0%';
                document.getElementById('val-right').textContent = '0%';

                applyTransform();
            }

            function applyTransform() {
                const imgEl = document.getElementById('modal-img');
                imgEl.style.transform = `rotate(${currentRotation}deg)`;
                imgEl.style.clipPath = `inset(${currentCropTop}% ${currentCropRight}% ${currentCropBottom}% ${currentCropLeft}%)`;
                
                updateEditorStatus();
            }

            function updateEditorStatus() {
                document.getElementById('editor-status').textContent = `Rot: ${currentRotation}° | Inset: T${currentCropTop}% R${currentCropRight}% B${currentCropBottom}% L${currentCropLeft}%`;
            }

            function renderEditedCanvas(callback) {
                const tempImg = new Image();
                
                // Only set crossOrigin if http/https
                if (currentImgSrc.startsWith('http')) {
                    tempImg.crossOrigin = 'anonymous';
                }
                
                tempImg.onload = function() {
                    try {
                        const rawW = tempImg.naturalWidth || tempImg.width || 1200;
                        const rawH = tempImg.naturalHeight || tempImg.height || 800;
                        
                        // Downscale max dimension to 1400px for lightweight canvas & fast local storage
                        const maxDim = 1400;
                        let scale = 1.0;
                        if (Math.max(rawW, rawH) > maxDim) {
                            scale = maxDim / Math.max(rawW, rawH);
                        }
                        
                        const iw = Math.floor(rawW * scale);
                        const ih = Math.floor(rawH * scale);
                        
                        const rad = currentRotation * Math.PI / 180;
                        const sin = Math.abs(Math.sin(rad));
                        const cos = Math.abs(Math.cos(rad));
                        
                        const rotW = Math.floor(iw * cos + ih * sin);
                        const rotH = Math.floor(iw * sin + ih * cos);
                        
                        const rotCanvas = document.createElement('canvas');
                        rotCanvas.width = rotW;
                        rotCanvas.height = rotH;
                        const rotCtx = rotCanvas.getContext('2d');
                        
                        rotCtx.translate(rotW / 2, rotH / 2);
                        rotCtx.rotate(rad);
                        rotCtx.drawImage(tempImg, -iw / 2, -ih / 2, iw, ih);
                        
                        // Apply 4-side crop insets
                        const cropX = Math.floor(rotW * (currentCropLeft / 100));
                        const cropY = Math.floor(rotH * (currentCropTop / 100));
                        const cropW = Math.floor(rotW * (1 - (currentCropLeft + currentCropRight) / 100));
                        const cropH = Math.floor(rotH * (1 - (currentCropTop + currentCropBottom) / 100));
                        
                        const finalCanvas = document.createElement('canvas');
                        finalCanvas.width = Math.max(10, cropW);
                        finalCanvas.height = Math.max(10, cropH);
                        const finalCtx = finalCanvas.getContext('2d');
                        
                        finalCtx.drawImage(rotCanvas, cropX, cropY, cropW, cropH, 0, 0, finalCanvas.width, finalCanvas.height);
                        
                        callback(finalCanvas);
                    } catch (err) {
                        console.error('Canvas render error:', err);
                    }
                };
                
                tempImg.onerror = function(err) {
                    console.error('Image load error:', err);
                };

                let rawSaved = null;
                try {
                    rawSaved = localStorage.getItem('saved_cert_' + currentImgSrc);
                } catch(e){}
                
                tempImg.src = rawSaved || currentImgSrc;
            }

            function saveAndApplyModalImg() {
                renderEditedCanvas(function(canvas) {
                    const dataUrl = canvas.toDataURL('image/jpeg', 0.90);
                    
                    try {
                        localStorage.setItem('saved_cert_' + currentImgSrc, dataUrl);
                    } catch(e) {
                        console.warn('LocalStorage quota limit reached, thumbnail updated in memory.');
                    }
                    
                    // Update live card thumbnail on webpage
                    const cardImgs = document.querySelectorAll(`img[src*="${currentImgSrc}"]`);
                    cardImgs.forEach(img => {
                        img.src = dataUrl;
                    });

                    // Update modal image display
                    const modalImg = document.getElementById('modal-img');
                    modalImg.src = dataUrl;
                    
                    // Reset CSS transforms since crop is now baked into the image
                    resetModalImg();

                    alert('Successfully saved and applied modifications!');
                });
            }

            function downloadEditedModalImg() {
                renderEditedCanvas(function(canvas) {
                    const link = document.createElement('a');
                    const cleanName = currentImgSrc.split('/').pop().split('?')[0];
                    link.download = `edited_${cleanName}`;
                    link.href = canvas.toDataURL('image/jpeg', 0.92);
                    link.click();
                });
            }

            // Restore any previously saved custom certificates on page load
            document.addEventListener('DOMContentLoaded', function() {
                const cardImgs = document.querySelectorAll('#credentials-grid img');
                cardImgs.forEach(img => {
                    const src = img.getAttribute('src');
                    if (src) {
                        try {
                            const saved = localStorage.getItem('saved_cert_' + src);
                            if (saved) {
                                img.src = saved;
                            }
                        } catch(e){}
                    }
                });
            });

            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape') {
                    closeCredentialModal();
                }
            });
        </script>'''

updated_html = re.sub(old_script_pattern, new_script_code, content, flags=re.DOTALL)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(updated_html)

print("Successfully injected optimized, quota-safe 4-side cropper and persistent save script into index.html!")
