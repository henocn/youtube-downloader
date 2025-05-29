#------------------------------------------------------------------#
#                     Tests de téléchargement YouTube Downloader  #
#------------------------------------------------------------------#
import sys
import os
import tempfile
import shutil
import time
from unittest.mock import patch, MagicMock
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main.downloader import YouTubeDownloader
from main.config import QUALITY_OPTIONS, AUDIO_FORMATS, VIDEO_FORMATS
from main.utils import print_success, print_error, print_info




#------------------------------------------------------------------#
#                     URLs de test                                #
#------------------------------------------------------------------#
TEST_URLS = {
    'video_courte': "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    'playlist_courte': "https://www.youtube.com/playlist?list=PLrAXtmRdnEQy6nuLMHjMZOz59Oq3KuQEl",
    'playlist_radio': "https://www.youtube.com/watch?v=4t5sbPQuYow&list=RD4t5sbPQuYow&start_radio=1",
    'video_inexistante': "https://www.youtube.com/watch?v=INEXISTANT123"
}




#------------------------------------------------------------------#
#                     Test d'initialisation du downloader         #
#------------------------------------------------------------------#
def test_downloader_initialization():
    print("=== Test d'initialisation du downloader ===")
    
    test_cases = [
        (None, "Chemin par défaut"),
        ("./custom_downloads", "Chemin personnalisé"),
        ("/tmp/test_downloads", "Chemin absolu")
    ]
    
    for path, description in test_cases:
        print(f"\nTest: {description}")
        
        try:
            if path:
                downloader = YouTubeDownloader(path)
                expected_path = os.path.abspath(path)
            else:
                downloader = YouTubeDownloader()
                expected_path = downloader.download_path
            
            if os.path.exists(downloader.download_path):
                print(f"  ✓ Downloader initialisé: {downloader.download_path}")
            else:
                print(f"  ✗ Répertoire non créé: {downloader.download_path}")
                
        except Exception as e:
            print(f"  ✗ Erreur d'initialisation: {e}")




#------------------------------------------------------------------#
#                     Test de récupération d'informations         #
#------------------------------------------------------------------#
def test_video_info_retrieval():
    print("\n=== Test de récupération d'informations ===")
    
    temp_dir = tempfile.mkdtemp()
    
    try:
        downloader = YouTubeDownloader(temp_dir)
        
        test_cases = [
            (TEST_URLS['video_courte'], "Vidéo courte"),
            (TEST_URLS['playlist_courte'], "Playlist courte"),
            (TEST_URLS['playlist_radio'], "Playlist radio"),
            (TEST_URLS['video_inexistante'], "Vidéo inexistante")
        ]
        
        for url, description in test_cases:
            print(f"\nTest: {description}")
            print(f"URL: {url[:50]}...")
            
            start_time = time.time()
            info = downloader.get_video_info(url)
            elapsed_time = time.time() - start_time
            
            if info:
                print(f"  ✓ Informations récupérées en {elapsed_time:.2f}s")
                print(f"    Titre: {info.get('title', 'N/A')[:40]}...")
                if 'video_count' in info:
                    print(f"    Nombre de vidéos: {info['video_count']}")
                else:
                    print(f"    Durée: {info.get('duration', 'N/A')}s")
                print(f"    Auteur: {info.get('uploader', 'N/A')[:30]}...")
            else:
                print(f"  ✗ Aucune information récupérée ({elapsed_time:.2f}s)")
    
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)




#------------------------------------------------------------------#
#                     Test de listing des formats                 #
#------------------------------------------------------------------#
def test_formats_listing():
    print("\n=== Test de listing des formats ===")
    
    temp_dir = tempfile.mkdtemp()
    
    try:
        downloader = YouTubeDownloader(temp_dir)
        
        test_cases = [
            (TEST_URLS['video_courte'], True, "Vidéo courte"),
            (TEST_URLS['playlist_courte'], False, "Playlist (devrait échouer)"),
            (TEST_URLS['video_inexistante'], False, "Vidéo inexistante")
        ]
        
        for url, should_work, description in test_cases:
            print(f"\nTest: {description}")
            print(f"URL: {url[:50]}...")
            
            start_time = time.time()
            formats = downloader.list_formats(url)
            elapsed_time = time.time() - start_time
            
            if formats and should_work:
                print(f"  ✓ {len(formats)} formats trouvés en {elapsed_time:.2f}s")
                print("    Exemples de formats:")
                for fmt in formats[:3]:
                    resolution = fmt.get('resolution', 'N/A')
                    ext = fmt.get('ext', 'N/A')
                    filesize = fmt.get('filesize', 0)
                    size_mb = f"{filesize/1024/1024:.1f}MB" if filesize else "N/A"
                    print(f"      {ext} | {resolution} | {size_mb}")
            elif not formats and not should_work:
                print(f"  ✓ Aucun format trouvé (attendu) en {elapsed_time:.2f}s")
            else:
                print(f"  ✗ Résultat inattendu en {elapsed_time:.2f}s")
    
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)




#------------------------------------------------------------------#
#                     Test de listing des vidéos de playlist      #
#------------------------------------------------------------------#
def test_playlist_videos_listing():
    print("\n=== Test de listing des vidéos de playlist ===")
    
    temp_dir = tempfile.mkdtemp()
    
    try:
        downloader = YouTubeDownloader(temp_dir)
        
        test_cases = [
            (TEST_URLS['playlist_courte'], True, "Playlist normale"),
            (TEST_URLS['playlist_radio'], True, "Playlist radio"),
            (TEST_URLS['video_courte'], False, "Vidéo simple (devrait échouer)")
        ]
        
        for url, should_work, description in test_cases:
            print(f"\nTest: {description}")
            print(f"URL: {url[:50]}...")
            
            start_time = time.time()
            videos = downloader.list_playlist_videos(url)
            elapsed_time = time.time() - start_time
            
            if videos and should_work:
                print(f"  ✓ {len(videos)} vidéos listées en {elapsed_time:.2f}s")
                print("    Premières vidéos:")
                for video in videos[:3]:
                    duration = f"{video['duration']//60}:{video['duration']%60:02d}" if video['duration'] else "N/A"
                    print(f"      {video['index']}. {video['title'][:30]}... ({duration})")
            elif not videos and not should_work:
                print(f"  ✓ Aucune vidéo listée (attendu) en {elapsed_time:.2f}s")
            else:
                print(f"  ✗ Résultat inattendu en {elapsed_time:.2f}s")
    
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)




#------------------------------------------------------------------#
#                     Test des options de téléchargement          #
#------------------------------------------------------------------#
def test_download_options():
    print("\n=== Test des options de téléchargement ===")
    
    temp_dir = tempfile.mkdtemp()
    
    try:
        downloader = YouTubeDownloader(temp_dir)
        
        test_cases = [
            ("best", "mp4", False, False, "Vidéo meilleure qualité"),
            ("worst", "mp4", False, False, "Vidéo pire qualité"),
            ("720p", "mp4", False, False, "Vidéo 720p"),
            ("best", "mp3", True, False, "Audio MP3"),
            ("best", "mp4", False, True, "Playlist limitée")
        ]
        
        for quality, format_type, audio_only, is_playlist, description in test_cases:
            print(f"\nTest: {description}")
            print(f"  Qualité: {quality}")
            print(f"  Format: {format_type}")
            print(f"  Audio seulement: {audio_only}")
            
            try:
                if is_playlist:
                    url = TEST_URLS['playlist_courte']
                    options = downloader._get_download_options(quality, format_type, audio_only, True, 1, 2)
                else:
                    url = TEST_URLS['video_courte']
                    options = downloader._get_download_options(quality, format_type, audio_only, False, 1, None)
                
                print(f"  ✓ Options générées:")
                print(f"    Format: {options.get('format', 'N/A')}")
                print(f"    Template: {os.path.basename(options.get('outtmpl', 'N/A'))}")
                
                if audio_only and 'postprocessors' in options:
                    print(f"    Post-traitement: Audio extraction")
                
            except Exception as e:
                print(f"  ✗ Erreur de génération d'options: {e}")
    
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)




#------------------------------------------------------------------#
#                     Test de simulation de téléchargement        #
#------------------------------------------------------------------#
def test_download_simulation():
    print("\n=== Test de simulation de téléchargement ===")
    
    temp_dir = tempfile.mkdtemp()
    
    try:
        downloader = YouTubeDownloader(temp_dir)
        
        test_cases = [
            (TEST_URLS['video_courte'], "worst", "mp4", False, "Vidéo test"),
            (TEST_URLS['playlist_courte'], "worst", "mp4", False, "Playlist test (2 vidéos)")
        ]
        
        for url, quality, format_type, audio_only, description in test_cases:
            print(f"\nTest: {description}")
            print(f"URL: {url[:50]}...")
            
            print_info("Mode simulation - pas de téléchargement réel")
            
            try:
                info = downloader.get_video_info(url)
                if info:
                    print("  ✓ URL accessible pour téléchargement")
                    print(f"    Titre: {info.get('title', 'N/A')[:40]}...")
                    
                    if 'video_count' in info:
                        print(f"    Nombre de vidéos: {info['video_count']}")
                    
                    options = downloader._get_download_options(
                        quality, format_type, audio_only, 
                        'video_count' in info, 1, 2 if 'video_count' in info else None
                    )
                    print("  ✓ Options de téléchargement validées")
                    
                else:
                    print("  ✗ URL inaccessible")
                    
            except Exception as e:
                print(f"  ✗ Erreur de simulation: {e}")
    
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)




#------------------------------------------------------------------#
#                     Test de gestion d'erreurs                   #
#------------------------------------------------------------------#
def test_error_handling():
    print("\n=== Test de gestion d'erreurs ===")
    
    temp_dir = tempfile.mkdtemp()
    
    try:
        downloader = YouTubeDownloader(temp_dir)
        
        error_cases = [
            (TEST_URLS['video_inexistante'], "Vidéo inexistante"),
            ("https://www.google.com", "URL non-YouTube"),
            ("", "URL vide"),
            ("not_a_url", "URL malformée")
        ]
        
        for url, description in error_cases:
            print(f"\nTest: {description}")
            print(f"URL: {url}")
            
            try:
                info = downloader.get_video_info(url)
                if info:
                    print("  ⚠ Informations récupérées (inattendu)")
                else:
                    print("  ✓ Erreur gérée correctement (aucune info)")
                    
                formats = downloader.list_formats(url)
                if formats:
                    print("  ⚠ Formats récupérés (inattendu)")
                else:
                    print("  ✓ Erreur gérée correctement (aucun format)")
                    
            except Exception as e:
                print(f"  ✓ Exception capturée: {type(e).__name__}")
    
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)




#------------------------------------------------------------------#
#                     Test de performance                         #
#------------------------------------------------------------------#
def test_performance():
    print("\n=== Test de performance ===")
    
    temp_dir = tempfile.mkdtemp()
    
    try:
        downloader = YouTubeDownloader(temp_dir)
        url = TEST_URLS['video_courte']
        
        operations = [
            ("Récupération d'informations", lambda: downloader.get_video_info(url)),
            ("Listing des formats", lambda: downloader.list_formats(url)),
        ]
        
        for operation_name, operation in operations:
            print(f"\nTest: {operation_name}")
            
            times = []
            for i in range(3):
                start_time = time.time()
                try:
                    result = operation()
                    elapsed_time = time.time() - start_time
                    times.append(elapsed_time)
                    print(f"  Essai {i+1}: {elapsed_time:.2f}s")
                except Exception as e:
                    print(f"  Essai {i+1}: Erreur - {e}")
            
            if times:
                avg_time = sum(times) / len(times)
                print(f"  Temps moyen: {avg_time:.2f}s")
                
                if avg_time < 5.0:
                    print("  ✓ Performance acceptable")
                else:
                    print("  ⚠ Performance lente")
    
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)




#------------------------------------------------------------------#
#                     Test de configuration                       #
#------------------------------------------------------------------#
def test_configuration_validation():
    print("\n=== Test de validation de configuration ===")
    
    print("Validation des qualités:")
    for quality in QUALITY_OPTIONS:
        format_value = QUALITY_OPTIONS[quality]
        print(f"  ✓ {quality}: {format_value}")
    
    print(f"\nFormats audio supportés: {len(AUDIO_FORMATS)}")
    for fmt in AUDIO_FORMATS:
        print(f"  ✓ {fmt}")
    
    print(f"\nFormats vidéo supportés: {len(VIDEO_FORMATS)}")
    for fmt in VIDEO_FORMATS:
        print(f"  ✓ {fmt}")
    
    temp_dir = tempfile.mkdtemp()
    
    try:
        downloader = YouTubeDownloader(temp_dir)
        
        print("\nTest de génération d'options:")
        test_configs = [
            ("best", "mp4", False),
            ("720p", "webm", False),
            ("worst", "mp3", True)
        ]
        
        for quality, format_type, audio_only in test_configs:
            try:
                options = downloader._get_download_options(quality, format_type, audio_only, False, 1, None)
                print(f"  ✓ {quality}/{format_type}/audio:{audio_only}")
            except Exception as e:
                print(f"  ✗ {quality}/{format_type}/audio:{audio_only} - {e}")
    
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)




#------------------------------------------------------------------#
#                     Fonction principale de test                 #
#------------------------------------------------------------------#
def run_download_tests():
    print("YouTube Downloader - Tests de téléchargement")
    print("=" * 60)
    
    test_downloader_initialization()
    test_video_info_retrieval()
    test_formats_listing()
    test_playlist_videos_listing()
    test_download_options()
    test_download_simulation()
    test_error_handling()
    test_performance()
    test_configuration_validation()
    
    print("\n" + "=" * 60)
    print("Tests de téléchargement terminés")




if __name__ == "__main__":
    run_download_tests()