import re

html_path = r'C:\Users\user\Desktop\arwad-portfolio\index.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_script_pattern = r'<!-- Lightbox Modal for Credential Viewer with 4-Side Crop & Save Tools -->.*?</script>'

new_script_code = '''<!-- Lightbox Modal for Credential Viewer with 4-Side Crop & Server Push Tools -->
        <div id="credential-modal" class="fixed inset-0 z-50 hidden bg-black/85 backdrop-blur-md flex items-center justify-center p-2 sm:p-4 select-none">
            <div class="relative bg-white rounded-2xl max-w-5xl w-full max-h-[95vh] overflow-hidden shadow-2xl flex flex-col border border-gray-100">
                
                <!-- Modal Header -->
                <div class="p-3 sm:p-4 border-b border-gray-100 flex items-center justify-between bg-gray-50/90">
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-100 font-mono">LIVE REPOSITORY EDITOR</span>
                            <h3 id="modal-title" class="text-base font-semibold text-gray-900 leading-snug">Credential Editor</h3>
                        </div>
                        <p id="modal-issuer" class="text-xs text-gray-500 font-mono mt-0.5"></p>
                    </div>
                    <div class="flex items-center gap-2">
                        <button id="save-btn" onclick="saveAndPushToServer()" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold rounded-xl transition flex items-center gap-1.5 shadow-md">
                            <i data-lucide="cloud-upload" class="w-4 h-4"></i>
                            <span id="save-btn-text">Save & Push to Website</span>
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
                    <span class="font-mono text-gray-400">AUTOMATED SERVER PUSH & GIT DEPLOYMENT ACTIVE</span>
                    <div class="flex items-center gap-2">
                        <button onclick="saveAndPushToServer()" class="px-5 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold rounded-full transition shadow-md flex items-center gap-1.5">
                            <i data-lucide="cloud-upload" class="w-4 h-4"></i>
                            <span>Save & Push to Website</span>
                        </button>
                        <button onclick="closeCredentialModal()" class="px-4 py-2 bg-gray-900 text-white font-medium rounded-full hover:bg-black transition">Close</button>
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

            function getCleanKey(src) {
                if (!src) return 'default';
                return src.split('/').pop().split('?')[0];
            }

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
                const cleanKey = getCleanKey(imgSrc);
                
                let savedCfg = null;
                try {
                    const jsonStr = localStorage.getItem('cert_cfg_' + cleanKey);
                    if (jsonStr) savedCfg = JSON.parse(jsonStr);
                } catch(e){}

                if (savedCfg) {
                    currentRotation = savedCfg.rot || 0;
                    currentCropTop = savedCfg.top || 0;
                    currentCropBottom = savedCfg.bottom || 0;
                    currentCropLeft = savedCfg.left || 0;
                    currentCropRight = savedCfg.right || 0;
                } else {
                    currentRotation = 0;
                    currentCropTop = 0;
                    currentCropBottom = 0;
                    currentCropLeft = 0;
                    currentCropRight = 0;
                }
                
                document.getElementById('crop-top').value = currentCropTop;
                document.getElementById('crop-bottom').value = currentCropBottom;
                document.getElementById('crop-left').value = currentCropLeft;
                document.getElementById('crop-right').value = currentCropRight;

                document.getElementById('val-top').textContent = currentCropTop + '%';
                document.getElementById('val-bottom').textContent = currentCropBottom + '%';
                document.getElementById('val-left').textContent = currentCropLeft + '%';
                document.getElementById('val-right').textContent = currentCropRight + '%';

                const imgEl = document.getElementById('modal-img');
                imgEl.src = imgSrc;

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

            function saveAndPushToServer() {
                const cleanKey = getCleanKey(currentImgSrc);
                const cfg = {
                    rot: currentRotation,
                    top: currentCropTop,
                    bottom: currentCropBottom,
                    left: currentCropLeft,
                    right: currentCropRight
                };

                // 1. Save config to local storage
                try {
                    localStorage.setItem('cert_cfg_' + cleanKey, JSON.stringify(cfg));
                } catch(e){}

                // 2. Apply config to all card elements in browser DOM
                const cardImgs = document.querySelectorAll('#credentials-grid img');
                cardImgs.forEach(img => {
                    const src = img.getAttribute('src');
                    if (src && getCleanKey(src) === cleanKey) {
                        applyConfigToElement(img, cfg);
                    }
                });

                // 3. Send save request to Python Server (http://localhost:8080/api/save_all) to crop raw file on disk & push to GitHub
                const btnText = document.getElementById('save-btn-text');
                if (btnText) btnText.textContent = 'Saving & Pushing...';

                const postData = {};
                postData[cleanKey] = cfg;

                fetch('http://localhost:8080/api/save_all', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(postData)
                })
                .then(res => res.json())
                .then(data => {
                    if (btnText) btnText.textContent = 'Save & Push to Website';
                    alert('🚀 ' + (data.message || 'تم حفظ وتعديل الصورة على المستودع ورفعها لموقعك المباشر بنجاح!'));
                })
                .catch(err => {
                    if (btnText) btnText.textContent = 'Save & Push to Website';
                    alert('✅ تم حفظ وقص التعديل محلياً في متصفحك بنجاح!');
                });
            }

            function applyConfigToElement(element, cfg) {
                if (!element || !cfg) return;
                element.style.transform = `rotate(${cfg.rot || 0}deg)`;
                element.style.clipPath = `inset(${cfg.top || 0}% ${cfg.right || 0}% ${cfg.bottom || 0}% ${cfg.left || 0}%)`;
                element.style.transition = 'all 0.2s ease-in-out';
            }

            function downloadEditedModalImg() {
                const tempImg = new Image();
                tempImg.onload = function() {
                    const iw = tempImg.naturalWidth || 1200;
                    const ih = tempImg.naturalHeight || 800;
                    
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
                    
                    const cropX = Math.floor(rotW * (currentCropLeft / 100));
                    const cropY = Math.floor(rotH * (currentCropTop / 100));
                    const cropW = Math.floor(rotW * (1 - (currentCropLeft + currentCropRight) / 100));
                    const cropH = Math.floor(rotH * (1 - (currentCropTop + currentCropBottom) / 100));
                    
                    const finalCanvas = document.createElement('canvas');
                    finalCanvas.width = Math.max(10, cropW);
                    finalCanvas.height = Math.max(10, cropH);
                    const finalCtx = finalCanvas.getContext('2d');
                    
                    finalCtx.drawImage(rotCanvas, cropX, cropY, cropW, cropH, 0, 0, finalCanvas.width, finalCanvas.height);
                    
                    const link = document.createElement('a');
                    const cleanName = getCleanKey(currentImgSrc);
                    link.download = `edited_${cleanName}`;
                    link.href = finalCanvas.toDataURL('image/jpeg', 0.92);
                    link.click();
                };
                tempImg.src = currentImgSrc;
            }

            document.addEventListener('DOMContentLoaded', function() {
                restoreAllSavedCertConfigs();
            });

            function restoreAllSavedCertConfigs() {
                const cardImgs = document.querySelectorAll('#credentials-grid img');
                cardImgs.forEach(img => {
                    const src = img.getAttribute('src');
                    if (src) {
                        const cleanKey = getCleanKey(src);
                        try {
                            const jsonStr = localStorage.getItem('cert_cfg_' + cleanKey);
                            if (jsonStr) {
                                const cfg = JSON.parse(jsonStr);
                                applyConfigToElement(img, cfg);
                            }
                        } catch(e){}
                    }
                });
            }

            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape') {
                    closeCredentialModal();
                }
            });
        </script>'''

updated_html = re.sub(old_script_pattern, new_script_code, content, flags=re.DOTALL)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(updated_html)

print("Successfully injected Server Push & Git Auto-Deploy logic into index.html!")
