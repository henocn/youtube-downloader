import os
import shutil
from datetime import datetime

def fix_file_encoding(filepath):
    """Corrige l'encodage d'un fichier"""
    backup_path = f"{filepath}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    try:
        # Sauvegarde
        shutil.copy2(filepath, backup_path)
        
        # Lecture avec détection automatique
        with open(filepath, 'rb') as f:
            raw_data = f.read()
        
        # Suppression du BOM si présent
        if raw_data.startswith(b'\xef\xbb\xbf'):  # UTF-8 BOM
            raw_data = raw_data[3:]
            print(f"  BOM UTF-8 supprimé de {filepath}")
        elif raw_data.startswith(b'\xff\xfe'):  # UTF-16 LE BOM
            raw_data = raw_data[2:]
            print(f"  BOM UTF-16 LE supprimé de {filepath}")
        elif raw_data.startswith(b'\xfe\xff'):  # UTF-16 BE BOM
            raw_data = raw_data[2:]
            print(f"  BOM UTF-16 BE supprimé de {filepath}")
        
        # Tentative de décodage avec différents encodages
        text_content = None
        encodings_to_try = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings_to_try:
            try:
                text_content = raw_data.decode(encoding)
                if encoding != 'utf-8':
                    print(f"  Fichier décodé avec {encoding}")
                break
            except UnicodeDecodeError:
                continue
        
        if text_content is None:
            print(f"❌ Impossible de décoder {filepath}")
            return False
        
        # Réécriture en UTF-8 sans BOM
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            f.write(text_content)
        
        print(f"✅ {filepath} corrigé")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction de {filepath}: {e}")
        # Restauration de la sauvegarde
        if os.path.exists(backup_path):
            shutil.move(backup_path, filepath)
        return False

def fix_all_files():
    """Corrige tous les fichiers problématiques"""
    from check_encoding import scan_project
    
    problematic_files = scan_project()
    
    if not problematic_files:
        print("Aucun fichier à corriger")
        return
    
    print(f"\n=== Correction de {len(problematic_files)} fichier(s) ===")
    
    for filepath in problematic_files:
        print(f"\nCorrection de {filepath}:")
        fix_file_encoding(filepath)

if __name__ == "__main__":
    fix_all_files()