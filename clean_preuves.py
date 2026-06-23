import os
import re

directory = 'competences'

for filename in os.listdir(directory):
    if not filename.endswith('.html'):
        continue
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # We want to process each sae-detail-card
    # A card starts with <div class="sae-detail-card and ends before the next card or the end of container
    cards = re.split(r'(<div class="sae-detail-card[^>]*>)', content)
    
    if len(cards) <= 1:
        continue
        
    new_content = cards[0]
    
    for i in range(1, len(cards), 2):
        card_start = cards[i]
        card_body = cards[i+1] if i+1 < len(cards) else ""
        
        # Find all a tags in this card that look like proofs
        a_tags = re.findall(r'<a href="\.\./img/preuves/[^>]+>.*?</a>', card_body, flags=re.DOTALL)
        
        # Deduplicate a_tags based on href
        unique_links = {}
        for tag in a_tags:
            match = re.search(r'href="([^"]+)"', tag)
            if match:
                href = match.group(1)
                if href not in unique_links:
                    unique_links[href] = tag
                    
        # Remove all existing sae-preuves blocks
        card_body_clean = re.sub(r'\s*<div class="sae-preuves".*?</div>\s*(?=</div>|\n\s*<div class="sae-preuves"|$)', '', card_body, flags=re.DOTALL)
        # But wait, the regex above might be greedy and remove the end of the card too.
        # A safer way to remove sae-preuves:
        # sae-preuves is a div, containing an h4 and a div with links, then closing two divs.
        card_body_clean = re.sub(r'\s*<div class="sae-preuves"[^>]*>.*?</div>\s*</div>', '', card_body, flags=re.DOTALL)
        
        # If we found links, we rebuild ONE sae-preuves block
        if unique_links:
            links_html = '\n            '.join(unique_links.values())
            preuves_block = f'''
        <div class="sae-preuves" style="margin-top:1.5rem; padding-top:1rem; border-top:1px solid rgba(255,255,255,0.1);">
          <h4 style="margin-bottom:0.5rem; color:#ccc;">Pièces jointes / Preuves</h4>
          <div style="display:flex; flex-wrap:wrap; gap:10px;">
            {links_html}
          </div>
        </div>
'''
            # Append it right before the last closing </div> of the card
            # The card_body_clean usually ends with </div>\n
            # Let's insert it before the last </div>
            last_div_index = card_body_clean.rfind('</div>')
            if last_div_index != -1:
                card_body_clean = card_body_clean[:last_div_index] + preuves_block + '      ' + card_body_clean[last_div_index:]
            else:
                card_body_clean += preuves_block

        new_content += card_start + card_body_clean
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
print("Nettoyage des preuves terminé.")
