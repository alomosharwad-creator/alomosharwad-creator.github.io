import re

html_path = r'C:\Users\user\Desktop\arwad-portfolio\index.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Build HTML for Project #01 Flagship AegisTwin-Vision
aegistwin_card = '''
                <!-- Project 01: AegisTwin-Vision (FLAGSHIP PROJECT & DEPLOYED) -->
                <div class="soft-card rounded-2xl p-7 flex flex-col justify-between relative overflow-hidden group border-2 border-indigo-500/30 shadow-md md:col-span-2 bg-gradient-to-r from-gray-900 to-indigo-950 text-white">
                    <div>
                        <div class="flex items-center justify-between mb-4">
                            <div class="flex items-center gap-2">
                                <span class="text-xs font-semibold uppercase tracking-wider text-emerald-400 bg-emerald-500/10 px-3 py-1 rounded-full border border-emerald-500/30 flex items-center gap-1.5 font-mono">
                                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span> Live & Open Source
                                </span>
                                <span class="text-xs font-semibold uppercase tracking-wider text-indigo-300 bg-indigo-500/20 px-3 py-1 rounded-full border border-indigo-500/40 font-mono">
                                    Flagship Platform
                                </span>
                            </div>
                            <span class="text-xs text-indigo-300 font-mono font-bold">#01</span>
                        </div>
                        <h3 class="serif-title text-3xl text-white mb-2.5 group-hover:text-indigo-400 transition">AegisTwin-Vision</h3>
                        <p class="text-sm text-gray-300 leading-relaxed mb-6 max-w-3xl">
                            Enterprise Digital Twin & Multi-Camera Edge AI Platform for Autonomous Industrial Robotics. Features real-time TensorRT-accelerated YOLOv8 multi-camera spatial tracking, 100Hz ROS2 6-DoF joint state telemetry, automated geo-fence hazard mitigation, sub-10ms emergency E-Stop triggers, and a bespoke glassmorphism industrial SaaS control dashboard.
                        </p>
                    </div>
                    <div>
                        <div class="flex flex-wrap gap-2 mb-6">
                            <span class="text-xs bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 px-3 py-1 rounded-md font-mono font-semibold">ROS 2 Telemetry</span>
                            <span class="text-xs bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 px-3 py-1 rounded-md font-mono font-semibold">Multi-Cam YOLOv8</span>
                            <span class="text-xs bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 px-3 py-1 rounded-md font-mono font-semibold">TensorRT FP16</span>
                            <span class="text-xs bg-rose-500/20 text-rose-300 border border-rose-500/30 px-3 py-1 rounded-md font-mono font-semibold">Spatial Geo-Fence</span>
                            <span class="text-xs bg-purple-500/20 text-purple-300 border border-purple-500/30 px-3 py-1 rounded-md font-mono font-semibold">6-DoF Kinematics</span>
                        </div>
                        <div class="flex flex-wrap items-center gap-4">
                            <a href="projects/aegistwin-vision/" target="_blank" class="inline-flex items-center gap-2 text-xs font-semibold px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white transition shadow-md">
                                <i data-lucide="play" class="w-3.5 h-3.5"></i>
                                <span>Launch Live Industrial Dashboard</span>
                            </a>
                            <a href="https://github.com/alomosharwad-creator/aegistwin-vision" target="_blank" class="inline-flex items-center gap-2 text-xs font-semibold text-gray-300 hover:text-white transition">
                                <span>View Source Code & Architecture</span>
                                <i data-lucide="external-link" class="w-3.5 h-3.5"></i>
                            </a>
                        </div>
                    </div>
                </div>'''

# Renumber old #01 to #02, #02 to #03, #03 to #04, #04 to #05, #05 to #06
content = re.sub(r'<!-- Project 1: OmniVision-RAG \(ACTIVE & DEPLOYED\) -->', r'<!-- Project 2: OmniVision-RAG (ACTIVE & DEPLOYED) -->', content)
content = re.sub(r'#01</span>', r'#02</span>', content)
content = re.sub(r'<!-- Project 2: PerceptoTrack \(ACTIVE & DEPLOYED\) -->', r'<!-- Project 3: PerceptoTrack (ACTIVE & DEPLOYED) -->', content)
content = re.sub(r'#02</span>', r'#03</span>', content)
content = re.sub(r'<!-- Project 3: AETHER \(ACTIVE & DEPLOYED\) -->', r'<!-- Project 4: AETHER (ACTIVE & DEPLOYED) -->', content)
content = re.sub(r'#03</span>', r'#04</span>', content)
content = re.sub(r'<!-- Project 4: DeepEdge-Assist \(ACTIVE & DEPLOYED\) -->', r'<!-- Project 5: DeepEdge-Assist (ACTIVE & DEPLOYED) -->', content)
content = re.sub(r'#04</span>', r'#05</span>', content)
content = re.sub(r'<!-- Project 5: Autonomous Fire-Fighting Robot \(GRADUATION THESIS\) -->', r'<!-- Project 6: Autonomous Fire-Fighting Robot (GRADUATION THESIS) -->', content)
content = re.sub(r'#05</span>', r'#06</span>', content)

# Insert AegisTwin card at start of grid
grid_anchor = r'(<div class="grid grid-cols-1 md:grid-cols-2 gap-6">)'
updated_content = re.sub(grid_anchor, r'\1' + aegistwin_card, content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(updated_content)

print("Successfully injected AegisTwin-Vision as Project #01 Flagship in index.html!")
