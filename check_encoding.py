import os
import chardet

def check_file_encoding(filepath):
    """Vérifie l'encodage d'un fichier"""
    try:
        with open(filepath, 'rb') as f:
            raw_data = f.read()
            
        # Détection automatique de l'encodage
        detected = chardet.detect(raw_data)
        
        # Vérification UTF-8
        try:
            raw_data.decode('utf-8')
            utf8_ok = True
        except UnicodeDecodeError:
            utf8_ok = False
            
        # Vérification BOM
        has_bom = raw_data.startswith(b'\xff\xfe') or raw_data.startswith(b'\xfe\xff') or raw_data.startswith(b'\xef\xbb\xbf')
        
        return {
            'file': filepath,
            'detected_encoding': detected['encoding'],
            'confidence': detected['confidence'],
            'utf8_compatible': utf8_ok,
            'has_bom': has_bom,
            'size': len(raw_data)
        }
    except Exception as e:
        return {
            'file': filepath,
            'error': str(e)
        }

def scan_project():
    """Scanne tous les fichiers du projet"""
    files_to_check = []
    
    for root, dirs, files in os.walk('.'):
        # Ignorer certains dossiers
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'env', 'venv', '.pytest_cache', 'build', 'dist']]
        
        for file in files:
            if file.endswith(('.py', '.md', '.txt', '.cfg', '.ini', '.toml')):
                filepath = os.path.join(root, file)
                files_to_check.append(filepath)
    
    print("=== Analyse des encodages ===")
    problematic_files = []
    
    for filepath in files_to_check:
        result = check_file_encoding(filepath)
        
        if 'error' in result:
            print(f"❌ {filepath}: ERREUR - {result['error']}")
            problematic_files.append(filepath)
        elif not result['utf8_compatible']:
            print(f"❌ {filepath}: Non UTF-8 - {result['detected_encoding']} ({result['confidence']:.2f})")
            problematic_files.append(filepath)
        elif result['has_bom']:
            print(f"⚠️  {filepath}: UTF-8 avec BOM")
            problematic_files.append(filepath)
        else:
            print(f"✅ {filepath}: UTF-8 OK")
    
    return problematic_files

if __name__ == "__main__":
    problematic = scan_project()
    
    if problematic:
        print(f"\n=== {len(problematic)} fichier(s) problématique(s) détecté(s) ===")
        for file in problematic:
            print(f"  - {file}")
    else:
        print("\n✅ Tous les fichiers sont compatibles UTF-8")