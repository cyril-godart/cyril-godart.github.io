import os
import glob
import re
import urllib.parse

html_dir = 'competences'
preuves_base = 'img/preuves/RESSOURCES'

mapping = {
    'R301': ['R3.01'],
    'R302': ['R3.02'],
    'R303': ['R3.03'],
    'R304': ['R3.04'],
    'R305': ['R3.05'],
    'R306': ['R3.06'],
    'R307': ['R3.07'],
    'R308': ['R3.08', 'R3.09'], # R3.08 & R3.09 are together in the html
    'R309': ['R3.08', 'R3.09'],
    'R310': ['R3.10'],
    'R401': ['R4.01'],
    'R402': ['R4.02', 'R4.03', 'R4.04'], # They are grouped
    'R403': ['R4.02', 'R4.03', 'R4.04'],
    'R404': ['R4.02', 'R4.03', 'R4.04'],
    'R4.Cyber9': ['R4.01', 'R4.Cyb.09'], # Grouped
    'R4.ROM10': ['R4.Cyb.10'],
    'SAE PENTEST': ['SAE 4.CYB.01'],
    'SAE301': ['SAE 3.01', 'SAE 301'],
    'SAE303': ['SAE 3.1.03'], # Assuming SAE 303 is QoS & Wi-Fi
    'SAE4ROM1': ['SAE 4 ROM.01'],
    'SAE TELEPHONIE': ['SAE 3'] # Unifier N1? We don't have a specific header, let's skip or add to Unifier
}

def get_files_for_folder(folder):
    path = os.path.join(preuves_base, folder)
    if not os.path.exists(path):
        return []
    # get all files recursively
    files = []
    for root, dirs, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith(('.pdf', '.png', '.jpg', '.jpeg', '.gif')):
                files.append(os.path.join(root, filename))
    return files

# Build a mapping of header -> list of files
header_files = {}
for folder, headers in mapping.items():
    files = get_files_for_folder(folder)
    for header in headers:
        if header not in header_files:
            header_files[header] = []
        header_files[header].extend(files)

for html_file in glob.glob(os.path.join(html_dir, '*.html')):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    changed = False
    
    # Find all sae-detail-card
    # We will use regex to find the card, then the header, then insert before the closing div of sae-content
    cards = re.split(r'(<div class="sae-detail-card.*?>)', content)
    new_content = cards[0]
    
    for i in range(1, len(cards), 2):
        card_start = cards[i]
        card_body = cards[i+1]
        
        # Check if this card has any of our headers
        matched_header = None
        for header, files in header_files.items():
            if header in card_body and len(files) > 0:
                matched_header = header
                break
        
        if matched_header:
            # Generate the HTML for proofs
            proofs_html = '\n        <div class="sae-preuves" style="margin-top:1.5rem; padding-top:1rem; border-top:1px solid rgba(255,255,255,0.1);">\n'
            proofs_html += '          <h4 style="margin-bottom:0.5rem; color:#ccc;">Pièces jointes / Preuves</h4>\n'
            proofs_html += '          <div style="display:flex; flex-wrap:wrap; gap:10px;">\n'
            
            # Deduplicate files
            files_to_add = list(set(header_files[matched_header]))
            
            for file_path in files_to_add:
                # Replace backslashes with forward slashes for web
                web_path = '../' + file_path.replace('\\', '/')
                # encode url components
                parts = web_path.split('/')
                encoded_parts = [urllib.parse.quote(p) for p in parts]
                web_path = '/'.join(encoded_parts)
                
                filename = os.path.basename(file_path)
                
                if file_path.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    proofs_html += f'            <a href="{web_path}" target="_blank" style="display:block; max-width:150px; overflow:hidden; border-radius:4px; border:1px solid #444;" title="{filename}"><img src="{web_path}" alt="{filename}" style="width:100%; height:auto; display:block;"></a>\n'
                else:
                    proofs_html += f'            <a href="{web_path}" target="_blank" class="btn-outline" style="font-size:0.85rem; padding:0.4rem 0.8rem; display:flex; align-items:center; gap:5px;"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg> {filename[:20]}...</a>\n'
            
            proofs_html += '          </div>\n        </div>\n      '
            
            # Insert proofs_html at the end of sae-content
            # sae-content ends with '</div>\n    </div>' (the card's closing div)
            # A safe way is to find the last '</div>' before the end of card_body if there is an sae-content
            if '<div class="sae-content">' in card_body or 'class="sae-skills-list"' in card_body:
                # split by closing divs, it's safer to just inject it before the last </div>
                parts = card_body.rsplit('</div>', 1)
                if len(parts) == 2:
                    card_body = parts[0] + proofs_html + '</div>' + parts[1]
                    changed = True

        new_content += card_start + card_body
        
    if changed:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {html_file}")

print("Done.")
