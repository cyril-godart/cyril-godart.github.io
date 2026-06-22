import os
import re
import pandas as pd
import PyPDF2
from constants import DATA_DIR

def search_in_text_file(filepath, keyword, is_regex=False):
    """
    Search for a keyword or regex in .txt, .html, .csv, etc.
    """
    results = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                match_found = False
                
                # Logique de recherche (Regex vs Texte simple)
                if is_regex:
                    if re.search(keyword, line, re.IGNORECASE):
                        match_found = True
                else:
                    if keyword.lower() in line.lower():
                        match_found = True

                if match_found:
                    clean_line = line.strip()[:100]  # Limit context length
                    results.append(f"Ligne {i + 1}: ...{clean_line}...")
                    
    except Exception as e:
        print(f"Error reading text file {filepath}: {e}")
    return results


def search_in_pdf(filepath, keyword, is_regex=False):
    """
    Search for a keyword or regex in a .pdf file using PyPDF2.
    """
    results = []
    try:
        with open(filepath, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    match_found = False
                    if is_regex:
                        if re.search(keyword, text, re.IGNORECASE):
                            match_found = True
                    else:
                        if keyword.lower() in text.lower():
                            match_found = True
                            
                    if match_found:
                        results.append(f"Page {page_num + 1}")
    except Exception as e:
        print(f"Error reading PDF {filepath}: {e}")
    return results


def search_in_excel(filepath, keyword, is_regex=False):
    """
    Search for a keyword in an .xlsx file using Pandas (All sheets).
    """
    results = []
    try:
        # sheet_name=None charge TOUTES les feuilles dans un dictionnaire
        dfs = pd.read_excel(filepath, sheet_name=None)
        
        for sheet_name, df in dfs.items():
            # Convert all data to string to search easily
            # Pandas .str.contains supports regex natively if regex=True
            mask = df.apply(lambda col: col.astype(str).str.contains(
                keyword, 
                case=False, 
                regex=is_regex, 
                na=False
            )).any(axis=1)
            
            matched_indices = df[mask].index.tolist()
            for idx in matched_indices:
                # On ajoute +2 car index 0 = ligne 2 dans Excel (après le header)
                results.append(f"Feuille '{sheet_name}' - Ligne {idx + 2}")
                
    except Exception as e:
        print(f"Error reading Excel {filepath}: {e}")
    return results


def search_all_files(keyword, is_regex=False):
    """
    Iterate recursively through DATA_DIR and apply searches.
    
    Args:
        keyword (str): The word or regex pattern.
        is_regex (bool): True to treat keyword as a regex pattern.
    """
    final_response = f"\n--- Résultats pour '{keyword}' (Regex: {is_regex}) ---\n"
    files_found = 0

    if not os.path.exists(DATA_DIR):
        return "Error: Data directory not found on server."

    # Remplacement de os.listdir par os.walk pour la récursivité
    for root, dirs, files in os.walk(DATA_DIR):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_results = []
            
            # Détection de l'extension
            ext = filename.split('.')[-1].lower()

            if ext in ['txt', 'html', 'htm', 'csv', 'json', 'xml', 'py']:
                file_results = search_in_text_file(filepath, keyword, is_regex)
            elif ext == 'pdf':
                file_results = search_in_pdf(filepath, keyword, is_regex)
            elif ext in ['xlsx', 'xls']:
                file_results = search_in_excel(filepath, keyword, is_regex)

            if file_results:
                files_found += 1
                # Affiche le chemin relatif pour plus de clarté
                rel_path = os.path.relpath(filepath, DATA_DIR)
                final_response += f"\nFichier: {rel_path}\n"
                for res in file_results:
                    final_response += f"  - {res}\n"

    if files_found == 0:
        return "Aucune correspondance trouvée."
    
    return final_response

# --- EXEMPLE D'UTILISATION (A supprimer si importé ailleurs) ---
if __name__ == "__main__":
    # Test recherche Regex (ex: adresse email)
    print(search_all_files(r"[a-zA-Z0-9._%+-]", is_regex=True))
    
    # Test recherche Simple
    # print(search_all_files("Facture", is_regex=False))