import os
import re

def insert_before_script(file_path, html_content):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We want to insert right before:
    #   </div>
    #   <script src="../js/script.js"></script>
    
    # Find the last occurrence of   </div>\n  <script
    pattern = r'  </div>\s*<script'
    match = list(re.finditer(pattern, content))
    if match:
        last_match = match[-1]
        new_content = content[:last_match.start()] + html_content + '\n' + content[last_match.start():]
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {file_path}")
    else:
        print(f"Could not find insertion point in {file_path}")

# Administrer
admin_html = """
    <div class="sae-detail-card theme-red">
      <div class="sae-header">
        <h2>R4.01 : Infrastructures de sécurité</h2>
        <span class="sae-tag">Ressource Semestre 4</span>
      </div>
      <p class="section-sub"><strong>AC validés :</strong> AC21.02</p>
      <div class="sae-content">
        <div class="sae-skills-list">
          <div class="sae-skill-item"><strong>Ce que j'ai fait :</strong> Configuration de pare-feux (Fortinet) et analyse de l'état de la menace (cryptographie asymétrique).</div>
          <div class="sae-skill-item"><strong>Pourquoi je l'ai fait :</strong> Pour protéger le système d'information et transformer les réseaux d'entreprise.</div>
          <div class="sae-skill-item"><strong>Ce que j'en ai appris :</strong> Les principes d'une architecture réseau sécurisée en entreprise.</div>
        </div>
      </div>
    </div>

    <div class="sae-detail-card theme-red">
      <div class="sae-header">
        <h2>R4.Cyb.09 : Sécurité des réseaux LAN</h2>
        <span class="sae-tag">Ressource Semestre 4</span>
      </div>
      <p class="section-sub"><strong>AC validés :</strong> AC21.02</p>
      <div class="sae-content">
        <div class="sae-skills-list">
          <div class="sae-skill-item"><strong>Ce que j'ai fait :</strong> Déploiement de protocoles de sécurité de niveau 2.</div>
          <div class="sae-skill-item"><strong>Pourquoi je l'ai fait :</strong> Pour empêcher les attaques internes sur le réseau local.</div>
        </div>
      </div>
    </div>

    <div class="sae-detail-card theme-red">
      <div class="sae-header">
        <h2>R4.Cyb.11 : Sécurisation de services réseaux</h2>
        <span class="sae-tag">Ressource Semestre 4</span>
      </div>
      <p class="section-sub"><strong>AC validés :</strong> AC21.04</p>
      <div class="sae-content">
        <div class="sae-skills-list">
          <div class="sae-skill-item"><strong>Ce que j'ai fait :</strong> Durcissement (hardening) de serveurs.</div>
          <div class="sae-skill-item"><strong>Comment je l'ai fait :</strong> Configuration avancée de pare-feux applicatifs et restriction des droits d'accès.</div>
        </div>
      </div>
    </div>
"""

# Connecter
connect_html = """
    <div class="sae-detail-card theme-orange">
      <div class="sae-header">
        <h2>R4.02 : Transmissions avancées</h2>
        <span class="sae-tag">Ressource Semestre 4</span>
      </div>
      <p class="section-sub"><strong>AC validés :</strong> AC22.01</p>
      <div class="sae-content">
        <div class="sae-skills-list">
          <div class="sae-skill-item"><strong>Ce que j'ai fait :</strong> Étude de la propagation à trajets multiples, OFDM, CDMA, OFDMA et MIMO.</div>
          <div class="sae-skill-item"><strong>Pourquoi je l'ai fait :</strong> Pour comprendre les modulations à étalement de spectre et les corrections d'erreurs.</div>
          <div class="sae-skill-item"><strong>Comment je l'ai fait :</strong> Mesures de taux d'erreurs et veille technologique (webinaire).</div>
        </div>
      </div>
    </div>

    <div class="sae-detail-card theme-orange">
      <div class="sae-header">
        <h2>R4.03 : Physique des Télécoms</h2>
        <span class="sae-tag">Ressource Semestre 4</span>
      </div>
      <p class="section-sub"><strong>AC validés :</strong> AC22.01</p>
      <div class="sae-content">
        <div class="sae-skills-list">
          <div class="sae-skill-item"><strong>Ce que j'ai fait :</strong> Caractérisation, mesure et déploiement de dispositifs radio ou optiques.</div>
          <div class="sae-skill-item"><strong>Pourquoi je l'ai fait :</strong> Ce sont des éléments indispensables aux transmissions modernes.</div>
          <div class="sae-skill-item"><strong>Ce que j'en ai appris :</strong> Les phénomènes de propagation des ondes (Abaque de Smith, MMANA, DVB-S).</div>
        </div>
      </div>
    </div>

    <div class="sae-detail-card theme-orange">
      <div class="sae-header">
        <h2>R4.04 : Réseaux cellulaires</h2>
        <span class="sae-tag">Ressource Semestre 4</span>
      </div>
      <p class="section-sub"><strong>AC validés :</strong> AC22.04</p>
      <div class="sae-content">
        <div class="sae-skills-list">
          <div class="sae-skill-item"><strong>Ce que j'ai fait :</strong> Étude des architectures 4G/5G et de leur déploiement.</div>
        </div>
      </div>
    </div>
"""

# Programmer
prog_html = """
    <div class="sae-detail-card theme-yellow">
      <div class="sae-header">
        <h2>R4.ROM.09 : Outils DevOps</h2>
        <span class="sae-tag">Ressource Semestre 4</span>
      </div>
      <p class="section-sub"><strong>AC validés :</strong> AC23.01</p>
      <div class="sae-content">
        <div class="sae-skills-list">
          <div class="sae-skill-item"><strong>Ce que j'ai fait :</strong> Utilisation d'outils d'intégration et déploiement continus (CI/CD).</div>
          <div class="sae-skill-item"><strong>Pourquoi je l'ai fait :</strong> Pour automatiser le cycle de vie du code réseau (Infrastructure as Code).</div>
        </div>
      </div>
    </div>
"""

# Restoring administrer-n2.html from git before injecting to remove my messed up insertion
os.system('git checkout competences/administrer-n2.html')

insert_before_script('competences/administrer-n2.html', admin_html)
insert_before_script('competences/connecter-n2.html', connect_html)
insert_before_script('competences/programmer-n2.html', prog_html)
