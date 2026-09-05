import re

html_path = r'C:\Users\user\Desktop\arwad-portfolio\index.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define the 23 exact credential cards
cards_data = [
    {
        "id": "IMG_0673.jpg",
        "cert_num": "CERT-01",
        "category": "technical",
        "cat_label": "AI & Technical",
        "cat_badge_cls": "bg-emerald-50 text-emerald-700 border-emerald-100",
        "title": "SUMO Robot Contest 2025 – Certificate of Participation",
        "issuer": "Hussein Technical University (HTU)",
        "desc": "Official certificate of participation and outstanding performance in the national SUMO Robot Contest 2025, awarded by HTU President Prof. Ismail Hinti."
    },
    {
        "id": "IMG_0674.jpg",
        "cert_num": "CERT-02",
        "category": "technical",
        "cat_label": "AI & Technical",
        "cat_badge_cls": "bg-emerald-50 text-emerald-700 border-emerald-100",
        "title": "Line Follower Robotics Specialist – Certificate of Attendance",
        "issuer": "JORA Robotics Academy",
        "desc": "Certificate awarded for completing intensive hands-on practical training in robotics electronics, 3D mechanical design, and autonomous line follower algorithms."
    },
    {
        "id": "IMG_0675.jpg",
        "cert_num": "CERT-03",
        "category": "technical",
        "cat_label": "AI & Technical",
        "cat_badge_cls": "bg-emerald-50 text-emerald-700 border-emerald-100",
        "title": "SHAI for AI – Certificate of Appreciation",
        "issuer": "SHAI (شاي) Artificial Intelligence Solutions",
        "desc": "Certificate of appreciation for contributing as a Machine Learning Developer & AI Trainer, delivering high-impact AI workshops and computer vision modules."
    },
    {
        "id": "IMG_0676.jpg",
        "cert_num": "CERT-04",
        "category": "technical",
        "cat_label": "AI & Technical",
        "cat_badge_cls": "bg-emerald-50 text-emerald-700 border-emerald-100",
        "title": "Applied AI & Practical Engineering Training Certificate",
        "issuer": "Al-Balqa Applied University & Industry Partners",
        "desc": "Training workshop completion certificate demonstrating advanced technical skills in machine learning model development and embedded system programming."
    },
    {
        "id": "IMG_0677.jpg",
        "cert_num": "CERT-05",
        "category": "ieee",
        "cat_label": "IEEE & Leadership",
        "cat_badge_cls": "bg-blue-50 text-blue-700 border-blue-100",
        "title": "Project 2 Market Exhibition & Competition Organizer (1st Edition)",
        "issuer": "Center for Innovation, Creativity & Entrepreneurship (BAU)",
        "desc": "Official certificate recognizing leadership in organizing the 1st annual Project 2 Market exhibition and competition held at BAU on month 5 3–5, 2024."
    },
    {
        "id": "IMG_0678.jpg",
        "cert_num": "CERT-06",
        "category": "ieee",
        "cat_label": "IEEE & Leadership",
        "cat_badge_cls": "bg-blue-50 text-blue-700 border-blue-100",
        "title": "National IEEE Engineering Hackathon – Certificate of Attendance",
        "issuer": "IEEE Jordan Section",
        "desc": "Certificate of participation recognizing active contribution to hackathon problem-solving and rapid prototyping in autonomous engineering systems."
    },
    {
        "id": "IMG_0679.jpg",
        "cert_num": "CERT-07",
        "category": "ieee",
        "cat_label": "IEEE & Leadership",
        "cat_badge_cls": "bg-blue-50 text-blue-700 border-blue-100",
        "title": "Project 2 Market Exhibition & Competition Organizer (2nd Edition)",
        "issuer": "Center for Innovation, Creativity & Entrepreneurship (BAU)",
        "desc": "Official commendation for directing technical logistics and event organization for the 2nd annual Project 2 Market exhibition on month 10 28–29, 2024."
    },
    {
        "id": "IMG_0680.jpg",
        "cert_num": "CERT-08",
        "category": "ieee",
        "cat_label": "IEEE & Leadership",
        "cat_badge_cls": "bg-blue-50 text-blue-700 border-blue-100",
        "title": "IEEE AESS Vice Chair & Executive Board Appointment",
        "issuer": "IEEE Aerospace & Electronic Systems Society",
        "desc": "Executive appointment badge as Vice Chair and General Events Coordinator for IEEE AESS Student Branch, overseeing technical seminars and student initiatives."
    },
    {
        "id": "IMG_0681.jpg",
        "cert_num": "CERT-09",
        "category": "technical",
        "cat_label": "AI & Technical",
        "cat_badge_cls": "bg-emerald-50 text-emerald-700 border-emerald-100",
        "title": "GrandTech Summit – Official Delegate & Tech Leader Credential",
        "issuer": "GrandTech Middle East Regional Technology Summit",
        "desc": "Official delegate badge for participating in regional AI innovation panels, robotics technology trends, and industry leadership networking."
    },
    {
        "id": "IMG_0682.jpg",
        "cert_num": "CERT-10",
        "category": "technical",
        "cat_label": "AI & Technical",
        "cat_badge_cls": "bg-emerald-50 text-emerald-700 border-emerald-100",
        "title": "Applied Machine Learning Course Instructor Commendation",
        "issuer": "Al-Balqa Applied University Student Chapter",
        "desc": "Recognition for organizing and instructing an intensive machine learning course for senior engineering students, covering computer vision and PyTorch fundamentals."
    },
    {
        "id": "IMG_0683.jpg",
        "cert_num": "CERT-11",
        "category": "ieee",
        "cat_label": "IEEE & Leadership",
        "cat_badge_cls": "bg-blue-50 text-blue-700 border-blue-100",
        "title": "IEEE Student Activities Committee (SAC) Jordan Section Leadership",
        "issuer": "IEEE Jordan Section SAC Team",
        "desc": "Leadership certificate for serving on the national IEEE Student Activities Committee, orchestrating nationwide student competitions and branch empowerment."
    },
    {
        "id": "IMG_0684.jpg",
        "cert_num": "CERT-12",
        "category": "ieee",
        "cat_label": "IEEE & Leadership",
        "cat_badge_cls": "bg-blue-50 text-blue-700 border-blue-100",
        "title": "TEDx Khilda Event Director & Logistics Leader Credential",
        "issuer": "TEDx Khilda Licensee Team",
        "desc": "Official organizer badge for managing venue logistics, speaker operations, and technical production for TEDx Khilda on month 8 16, 2025."
    },
    {
        "id": "IMG_0685.jpg",
        "cert_num": "CERT-13",
        "category": "technical",
        "cat_label": "AI & Technical",
        "cat_badge_cls": "bg-emerald-50 text-emerald-700 border-emerald-100",
        "title": "Project 2 Market Innovation Finalist Commendation",
        "issuer": "Innovation & Entrepreneurship Center (BAU)",
        "desc": "Recognition for pitching AI-driven hardware solutions and autonomous systems to regional venture capital panels and industrial judges."
    },
    {
        "id": "IMG_0686.jpg",
        "cert_num": "CERT-14",
        "category": "humanitarian",
        "cat_label": "Humanitarian & Civic",
        "cat_badge_cls": "bg-amber-50 text-amber-700 border-amber-100",
        "title": "TEDx Amman Official Operations & Usher Leader Pass",
        "issuer": "TEDx Amman Organizing Committee",
        "desc": "Operations leadership credential for managing venue flow, guest experience, and stage coordination at TEDx Amman under the theme 'Where Ideas Meet History'."
    },
    {
        "id": "IMG_0687.jpg",
        "cert_num": "CERT-15",
        "category": "ieee",
        "cat_label": "IEEE & Leadership",
        "cat_badge_cls": "bg-blue-50 text-blue-700 border-blue-100",
        "title": "IEEE BAU Student Branch Executive Delegate Badge",
        "issuer": "IEEE Student Branch Al-Balqa Applied University",
        "desc": "Executive officer pass representing IEEE BAU branch across national technology congresses, student branch officer training, and robotics hackathons."
    },
    {
        "id": "IMG_0688.jpg",
        "cert_num": "CERT-16",
        "category": "ieee",
        "cat_label": "IEEE & Leadership",
        "cat_badge_cls": "bg-blue-50 text-blue-700 border-blue-100",
        "title": "JSYP Congress Official Delegate Badge (ID: 191)",
        "issuer": "Jordan Student & Young Professionals (JSYP) Congress",
        "desc": "Official delegate badge for participating in national engineering leadership workshops, career mentorship, and technical innovation summits."
    },
    {
        "id": "IMG_0689.jpg",
        "cert_num": "CERT-17",
        "category": "technical",
        "cat_label": "AI & Technical",
        "cat_badge_cls": "bg-emerald-50 text-emerald-700 border-emerald-100",
        "title": "Amman Arab University National Robotics Competition Award",
        "issuer": "Amman Arab University & JRA Robotics",
        "desc": "Award certificate for competing in the national robotics championship, designing custom control hardware and autonomous navigation logic."
    },
    {
        "id": "IMG_0690.jpg",
        "cert_num": "CERT-18",
        "category": "humanitarian",
        "cat_label": "Humanitarian & Civic",
        "cat_badge_cls": "bg-amber-50 text-amber-700 border-amber-100",
        "title": "Humanitarian STEM Educator & Community Relief Certificate",
        "issuer": "National Civic Service & Orphan Care Initiatives",
        "desc": "Commendation for teaching STEM and physics to Gaza secondary school students during crisis relief, and mentoring youth at local orphan care centers."
    },
    {
        "id": "IMG_0691.jpg",
        "cert_num": "CERT-19",
        "category": "technical",
        "cat_label": "AI & Technical",
        "cat_badge_cls": "bg-emerald-50 text-emerald-700 border-emerald-100",
        "title": "Google Developer Groups DevFest Amman 2024 Lead Pass",
        "issuer": "Google Developer Groups (GDG) Amman",
        "desc": "Official event lead pass for organizing DevFest Amman 2024, facilitating developer workshops on AI models, Google Cloud, and machine learning tools."
    },
    {
        "id": "IMG_0692.jpg",
        "cert_num": "CERT-20",
        "category": "technical",
        "cat_label": "AI & Technical",
        "cat_badge_cls": "bg-emerald-50 text-emerald-700 border-emerald-100",
        "title": "National SUMO Robotics Championship Contestant Badge (Botzilla)",
        "issuer": "Jordan Robotics Academy & HTU",
        "desc": "Contestant credential for team 'Botzilla - JRA', engineering high-torque autonomous combat robots for national sumo wrestling robot trials."
    },
    {
        "id": "IMG_0693.jpg",
        "cert_num": "CERT-21",
        "category": "technical",
        "cat_label": "AI & Technical",
        "cat_badge_cls": "bg-emerald-50 text-emerald-700 border-emerald-100",
        "title": "Computer Vision & Edge Computing Masterclass Certificate",
        "issuer": "Advanced AI & Embedded Vision Workshop",
        "desc": "Certificate of accomplishment in implementing real-time Object Detection (YOLO), OpenCV image processing, and Edge AI deployment on embedded hardware."
    },
    {
        "id": "IMG_0694.jpg",
        "cert_num": "CERT-22",
        "category": "technical",
        "cat_label": "AI & Technical",
        "cat_badge_cls": "bg-emerald-50 text-emerald-700 border-emerald-100",
        "title": "Academic Excellence & B.Sc. Graduation Thesis Commendation",
        "issuer": "Faculty of Engineering, Al-Balqa Applied University",
        "desc": "Academic recognition for capstone engineering research in AI, Autonomous Navigation, and Robotics, achieving high evaluation from university faculty."
    },
    {
        "id": "IMG_0695.jpg",
        "cert_num": "CERT-23",
        "category": "ieee",
        "cat_label": "IEEE & Leadership",
        "cat_badge_cls": "bg-blue-50 text-blue-700 border-blue-100",
        "title": "Project 2 Market Official Event Director & General Organizer Pass",
        "issuer": "Center for Innovation & Entrepreneurship (BAU)",
        "desc": "Executive organizer badge for overseeing overall event strategy, university administration alignment, and participant logistics for Project 2 Market."
    }
]

# Build HTML string for credentials grid
cards_html = []
for c in cards_data:
    img_path = f"assets/certificates/{c['id']}"
    # Escape quotes for JS onclick call
    js_title = c['title'].replace("'", "\\'")
    js_issuer = c['issuer'].replace("'", "\\'")
    
    card_str = f'''                <div class="soft-card rounded-2xl p-5 flex flex-col justify-between group cred-card" data-category="{c['category']}">
                    <div>
                        <div class="relative overflow-hidden rounded-xl bg-gray-100 mb-4 h-52 flex items-center justify-center cursor-pointer border border-gray-100 shadow-sm" onclick="openCredentialModal('{img_path}', '{js_title}', '{js_issuer}')">
                            <img src="{img_path}" alt="{c['title']}" class="w-full h-full object-cover group-hover:scale-105 transition duration-300">
                            <div class="absolute inset-0 bg-black/30 opacity-0 group-hover:opacity-100 transition flex items-center justify-center text-white text-xs font-semibold gap-1.5">
                                <i data-lucide="maximize-2" class="w-4 h-4"></i> Expand Credential
                            </div>
                        </div>
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-xs font-semibold px-2.5 py-0.5 rounded-full border {c['cat_badge_cls']}">
                                {c['cat_label']}
                            </span>
                            <span class="text-xs text-gray-400 font-mono">{c['cert_num']}</span>
                        </div>
                        <h4 class="text-base font-semibold text-gray-900 mb-1 leading-snug group-hover:text-indigo-600 transition">{c['title']}</h4>
                        <p class="text-xs font-mono text-gray-500 mb-3">{c['issuer']}</p>
                        <p class="text-xs text-gray-600 leading-relaxed mb-4">{c['desc']}</p>
                    </div>
                    <div>
                        <button onclick="openCredentialModal('{img_path}', '{js_title}', '{js_issuer}')" class="w-full py-2.5 px-4 rounded-xl border border-gray-200 hover:border-gray-900 bg-white text-gray-900 text-xs font-semibold transition flex items-center justify-center gap-2">
                            <i data-lucide="file-check" class="w-3.5 h-3.5 text-indigo-600"></i>
                            <span>View High-Res Document</span>
                        </button>
                    </div>
                </div>'''
    cards_html.append(card_str)

new_grid_content = "\n\n".join(cards_html)

# Pattern to replace grid contents
pattern = r'(<div class="grid grid-cols-1 md:grid-cols-3 gap-6" id="credentials-grid">)(.*?)(</div>\s*</div>\s*</section>)'
match = re.search(pattern, content, re.DOTALL)

if match:
    updated_content = content[:match.start(2)] + "\n\n" + new_grid_content + "\n\n            " + content[match.start(3):]
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    print("Successfully updated index.html with all 23 exact credential cards!")
else:
    print("Could not find credentials-grid in index.html!")
