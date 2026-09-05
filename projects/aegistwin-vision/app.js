// AegisTwin-Vision Enterprise Engine
document.addEventListener('DOMContentLoaded', () => {
  initVisionCanvas();
  initDigitalTwinCanvas();
  initMetricsLoop();
  initControls();
});

let isEStopped = false;
let activeCam = 'cam-1';

// Vision Canvas Pipeline Simulation
function initVisionCanvas() {
  const canvas = document.getElementById('vision-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  
  let frameCount = 0;
  
  // Simulated tracked entities
  const entities = [
    { id: 'HUMAN_01', type: 'person', x: 120, y: 140, vx: 1.2, vy: 0.5, label: 'Operator (Arwad A.)', risk: 'LOW' },
    { id: 'AGV_04', type: 'agv', x: 380, y: 220, vx: -0.8, vy: 0.2, label: 'AGV Heavy Transport', risk: 'LOW' },
    { id: 'ARM_CELL_A', type: 'hazard_zone', x: 260, y: 80, w: 220, h: 200, label: '6-DoF Arm Cell Safety Zone' }
  ];

  function draw() {
    frameCount++;
    const w = canvas.width;
    const h = canvas.height;
    
    // Clear background
    ctx.fillStyle = '#060911';
    ctx.fillRect(0, 0, w, h);
    
    // Draw Grid Lines
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.04)';
    ctx.lineWidth = 1;
    const gridSize = 40;
    for (let x = 0; x < w; x += gridSize) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, h);
      ctx.stroke();
    }
    for (let y = 0; y < h; y += gridSize) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(w, y);
      ctx.stroke();
    }
    
    // Draw Safety Geo-Fence Zone
    const zone = entities[2];
    ctx.strokeStyle = isEStopped ? 'rgba(244, 63, 94, 0.8)' : 'rgba(245, 158, 11, 0.5)';
    ctx.fillStyle = isEStopped ? 'rgba(244, 63, 94, 0.12)' : 'rgba(245, 158, 11, 0.05)';
    ctx.lineWidth = 2;
    ctx.setLineDash([6, 4]);
    ctx.fillRect(zone.x, zone.y, zone.w, zone.h);
    ctx.strokeRect(zone.x, zone.y, zone.w, zone.h);
    ctx.setLineDash([]);
    
    ctx.fillStyle = isEStopped ? '#f43f5e' : '#f59e0b';
    ctx.font = '10px "JetBrains Mono", monospace';
    ctx.fillText('⚠ HIGH-RISK ROBOTIC CELL GEO-FENCE', zone.x + 8, zone.y + 16);
    
    // Update and draw entities
    entities.forEach(ent => {
      if (ent.type === 'hazard_zone') return;
      
      if (!isEStopped) {
        ent.x += ent.vx;
        ent.y += ent.vy;
        if (ent.x < 40 || ent.x > w - 120) ent.vx *= -1;
        if (ent.y < 40 || ent.y > h - 100) ent.vy *= -1;
      }
      
      // Check if Human inside hazard zone
      const insideZone = (
        ent.type === 'person' &&
        ent.x > zone.x && ent.x < zone.x + zone.w &&
        ent.y > zone.y && ent.y < zone.y + zone.h
      );
      
      const boxColor = insideZone ? '#f43f5e' : (ent.type === 'person' ? '#06b6d4' : '#10b981');
      const boxW = ent.type === 'person' ? 60 : 100;
      const boxH = ent.type === 'person' ? 110 : 70;
      
      // Bounding Box
      ctx.strokeStyle = boxColor;
      ctx.lineWidth = 2;
      ctx.strokeRect(ent.x, ent.y, boxW, boxH);
      
      // Corner Brackets
      const bLen = 8;
      ctx.lineWidth = 3;
      // Top-Left
      ctx.beginPath(); ctx.moveTo(ent.x, ent.y + bLen); ctx.lineTo(ent.x, ent.y); ctx.lineTo(ent.x + bLen, ent.y); ctx.stroke();
      // Top-Right
      ctx.beginPath(); ctx.moveTo(ent.x + boxW - bLen, ent.y); ctx.lineTo(ent.x + boxW, ent.y); ctx.lineTo(ent.x + boxW, ent.y + bLen); ctx.stroke();
      
      // Label Tag
      ctx.fillStyle = boxColor;
      ctx.fillRect(ent.x, ent.y - 18, boxW, 18);
      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 9px "JetBrains Mono", monospace';
      const conf = (94.2 + (frameCount % 10) * 0.4).toFixed(1);
      ctx.fillText(`${ent.id} ${conf}%`, ent.x + 4, ent.y - 5);
      
      // Distance Vector to Robot Arm Base
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
      ctx.lineWidth = 1;
      ctx.setLineDash([3, 3]);
      ctx.beginPath();
      ctx.moveTo(ent.x + boxW/2, ent.y + boxH/2);
      ctx.lineTo(zone.x + zone.w/2, zone.y + zone.h/2);
      ctx.stroke();
      ctx.setLineDash([]);
      
      // Distance label
      const dist = Math.hypot((ent.x + boxW/2) - (zone.x + zone.w/2), (ent.y + boxH/2) - (zone.y + zone.h/2)) / 30;
      ctx.fillStyle = '#9ca3af';
      ctx.font = '9px "JetBrains Mono", monospace';
      ctx.fillText(`${dist.toFixed(2)}m`, (ent.x + zone.x + zone.w/2)/2, (ent.y + zone.y + zone.h/2)/2);
    });
    
    // Status Overlay Text
    ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
    ctx.font = '10px "JetBrains Mono", monospace';
    ctx.fillText(`CAM_FEED: ACTIVE [${activeCam.toUpperCase()}]`, 12, h - 15);
    ctx.fillText(`YOLOv8x-POSE // INFERENCE: 8.4ms`, w - 240, h - 15);
    
    requestAnimationFrame(draw);
  }
  
  draw();
}

// Digital Twin Canvas Simulation (ROS2 6-DoF Arm Kinematics)
function initDigitalTwinCanvas() {
  const canvas = document.getElementById('twin-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  
  let angle = 0;
  
  function draw() {
    if (!isEStopped) {
      angle += 0.02;
    }
    
    const w = canvas.width;
    const h = canvas.height;
    
    ctx.fillStyle = '#070b14';
    ctx.fillRect(0, 0, w, h);
    
    // Base center
    const baseX = w / 2;
    const baseY = h - 50;
    
    // Draw Base Pedestal
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(baseX - 40, baseY, 80, 25);
    ctx.strokeStyle = '#334155';
    ctx.lineWidth = 2;
    ctx.strokeRect(baseX - 40, baseY, 80, 25);
    
    // Kinematic Joints
    const L1 = 90;
    const L2 = 80;
    const L3 = 50;
    
    const theta1 = -Math.PI / 2 + Math.sin(angle) * 0.4;
    const theta2 = Math.cos(angle * 1.3) * 0.5;
    const theta3 = Math.sin(angle * 0.8) * 0.6;
    
    const x1 = baseX + L1 * Math.cos(theta1);
    const y1 = baseY + L1 * Math.sin(theta1);
    
    const x2 = x1 + L2 * Math.cos(theta1 + theta2);
    const y2 = y1 + L2 * Math.sin(theta1 + theta2);
    
    const x3 = x2 + L3 * Math.cos(theta1 + theta2 + theta3);
    const y3 = y2 + L3 * Math.sin(theta1 + theta2 + theta3);
    
    // Draw Link 1
    ctx.strokeStyle = '#6366f1';
    ctx.lineWidth = 10;
    ctx.lineCap = 'round';
    ctx.beginPath();
    ctx.moveTo(baseX, baseY);
    ctx.lineTo(x1, y1);
    ctx.stroke();
    
    // Draw Link 2
    ctx.strokeStyle = '#06b6d4';
    ctx.lineWidth = 7;
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();
    
    // Draw Link 3 (End-Effector)
    ctx.strokeStyle = '#10b981';
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(x2, y2);
    ctx.lineTo(x3, y3);
    ctx.stroke();
    
    // Draw Joint Nodes
    [ {x: baseX, y: baseY}, {x: x1, y: y1}, {x: x2, y: y2}, {x: x3, y: y3} ].forEach((joint, idx) => {
      ctx.fillStyle = idx === 3 ? '#f43f5e' : '#ffffff';
      ctx.beginPath();
      ctx.arc(joint.x, joint.y, idx === 3 ? 6 : 7, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = '#0f172a';
      ctx.lineWidth = 2;
      ctx.stroke();
    });
    
    // Update Joint Angle Labels in DOM
    const j1El = document.getElementById('joint-1-val');
    const j2El = document.getElementById('joint-2-val');
    const j3El = document.getElementById('joint-3-val');
    const eeEl = document.getElementById('ee-pos-val');
    
    if (j1El) j1El.textContent = `${(theta1 * 180 / Math.PI).toFixed(1)}°`;
    if (j2El) j2El.textContent = `${(theta2 * 180 / Math.PI).toFixed(1)}°`;
    if (j3El) j3El.textContent = `${(theta3 * 180 / Math.PI).toFixed(1)}°`;
    if (eeEl) eeEl.textContent = `[${x3.toFixed(0)}, ${y3.toFixed(0)}, ${(120 + Math.sin(angle)*20).toFixed(0)}]`;
    
    requestAnimationFrame(draw);
  }
  
  draw();
}

// Live Metrics & Telemetry Updater Loop
function initMetricsLoop() {
  setInterval(() => {
    const fpsEl = document.getElementById('val-fps');
    const latEl = document.getElementById('val-lat');
    const queueEl = document.getElementById('val-queue');
    const cpuEl = document.getElementById('val-cpu');
    
    if (fpsEl) fpsEl.textContent = isEStopped ? '0.0' : (59.2 + Math.random() * 1.5).toFixed(1);
    if (latEl) latEl.textContent = (8.1 + Math.random() * 0.6).toFixed(1);
    if (queueEl) queueEl.textContent = Math.floor(2 + Math.random() * 3);
    if (cpuEl) cpuEl.textContent = `${(32 + Math.random() * 4).toFixed(1)}%`;
  }, 1000);
}

// Interactive Controls & Camera Switcher
function initControls() {
  const estopBtn = document.getElementById('estop-btn');
  if (estopBtn) {
    estopBtn.addEventListener('click', () => {
      isEStopped = !isEStopped;
      if (isEStopped) {
        estopBtn.classList.remove('bg-rose-600', 'hover:bg-rose-500');
        estopBtn.classList.add('bg-amber-600', 'hover:bg-amber-500');
        estopBtn.innerHTML = '<i data-lucide="play" class="w-4 h-4"></i><span>RESUME SYSTEM</span>';
        updateSystemStatus('E-STOP ACTIVE - SYSTEM HALTED', 'rose');
      } else {
        estopBtn.classList.remove('bg-amber-600', 'hover:bg-amber-500');
        estopBtn.classList.add('bg-rose-600', 'hover:bg-rose-500');
        estopBtn.innerHTML = '<i data-lucide="square" class="w-4 h-4"></i><span>EMERGENCY E-STOP</span>';
        updateSystemStatus('NOMINAL - SYSTEM ACTIVE', 'emerald');
      }
      if (window.lucide) lucide.createIcons();
    });
  }
  
  // Camera feed buttons
  const camBtns = document.querySelectorAll('.cam-btn');
  camBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      camBtns.forEach(b => b.classList.remove('bg-indigo-600', 'text-white'));
      btn.classList.add('bg-indigo-600', 'text-white');
      activeCam = btn.getAttribute('data-cam');
    });
  });
}

function updateSystemStatus(text, color) {
  const badge = document.getElementById('sys-status-badge');
  if (badge) {
    badge.textContent = text;
    badge.className = `px-3 py-1 rounded-full text-xs font-mono font-semibold border bg-${color}-500/10 text-${color}-400 border-${color}-500/30 flex items-center gap-2`;
  }
}
