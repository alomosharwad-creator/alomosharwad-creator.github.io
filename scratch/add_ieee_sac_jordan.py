import re

html_path = r'C:\Users\user\Desktop\arwad-portfolio\index.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. New Experience Cards HTML for #experience section
new_exp_cards = '''
                <div class="flex flex-col sm:flex-row sm:items-baseline justify-between gap-1 pb-6 border-b border-gray-100/70">
                    <div class="max-w-2xl">
                        <div class="flex items-center gap-2 mb-1">
                            <span class="text-xs bg-blue-50 text-blue-700 font-semibold px-2 py-0.5 rounded-full border border-blue-100">National IEEE Leadership</span>
                        </div>
                        <h4 class="text-base font-semibold text-gray-900">Vice Chair of Media & Public Relations — IEEE SAC Jordan Section</h4>
                        <p class="text-xs font-mono text-gray-500 mb-2.5">IEEE Jordan Section · Student Activities Committee (SAC)</p>
                        <ul class="text-sm text-gray-600 space-y-1 leading-relaxed">
                            <li>• Directed nationwide media strategy, public relations campaigns, and digital communications engaging student chapters across all Jordanian universities.</li>
                            <li>• Orchestrated national branding, media outreach, and leadership empowerment summits for student engineering chapters.</li>
                        </ul>
                    </div>
                    <span class="text-xs text-gray-400 font-mono mt-1 sm:mt-0 whitespace-nowrap">2024 – Present</span>
                </div>

                <div class="flex flex-col sm:flex-row sm:items-baseline justify-between gap-1 pb-6 border-b border-gray-100/70">
                    <div class="max-w-2xl">
                        <div class="flex items-center gap-2 mb-1">
                            <span class="text-xs bg-blue-50 text-blue-700 font-semibold px-2 py-0.5 rounded-full border border-blue-100">Section Coordination</span>
                        </div>
                        <h4 class="text-base font-semibold text-gray-900">Executive Committee Coordinator & Member — IEEE Jordan Section</h4>
                        <p class="text-xs font-mono text-gray-500 mb-2.5">IEEE Jordan Section Executive Committee</p>
                        <ul class="text-sm text-gray-600 space-y-1 leading-relaxed">
                            <li>• Coordinated national engineering symposiums, cross-university student robotics competitions, and branch development initiatives under IEEE Jordan Section.</li>
                            <li>• Facilitated inter-university technical collaboration, officer training workshops, and nationwide student branch operations.</li>
                        </ul>
                    </div>
                    <span class="text-xs text-gray-400 font-mono mt-1 sm:mt-0 whitespace-nowrap">2023 – Present</span>
                </div>'''

# Inject into #experience section after line 294
exp_anchor = r'(<section id="experience" class="mb-24 scroll-mt-24">\s*<h2 class="serif-title text-3xl font-normal text-gray-950 mb-10 pb-4 border-b border-gray-100">Engineering & Academic Experience</h2>\s*<div class="space-y-8">)'

updated_content = re.sub(exp_anchor, r'\1' + new_exp_cards, content, flags=re.DOTALL)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(updated_content)

print("Successfully added IEEE SAC Vice Chair Media & IEEE Jordan Section Executive Coordinator roles to index.html!")
