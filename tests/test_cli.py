#------------------------------------------------------------------#
#                     Tests CLI YouTube Downloader                #
#------------------------------------------------------------------#
import sys
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main.cli import main, show_video_info, show_available_formats, show_playlist_videos
from main.downloader import YouTubeDownloader
from main.utils import is_valid_youtube_url, is_playlist_url, get_playlist_type




#------------------------------------------------------------------#
#                     URLs de test                                #
#------------------------------------------------------------------#
TEST_URLS = {
    'video_simple': "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    'playlist_normale': "https://www.youtube.com/playlist?list=PLrAXtmRdnEQy6nuLMHjMZOz59Oq3KuQEl",
    'playlist_radio': "https://www.youtube.com/watch?v=4t5sbPQuYow&list=RD4t5sbPQuYow&start_radio=1",
    'url_invalide': "https://www.google.com"
}




#------------------------------------------------------------------#
#                     Test des fonctions utilitaires CLI          #
#------------------------------------------------------------------#
def test_url_validation():
    print("=== Test de validation d'URL CLI ===")
    
    test_cases = [
        (TEST_URLS['video_simple'], True, "Vidéo YouTube valide"),
        (TEST_URLS['playlist_normale'], True, "Playlist normale valide"),
        (TEST_URLS['playlist_radio'], True, "Playlist radio valide"),
        (TEST_URLS['url_invalide'], False, "URL non-YouTube"),
        ("", False, "URL vide"),
        ("not_a_url", False, "Chaîne invalide")
    ]
    
    for url, expected, description in test_cases:
        result = is_valid_youtube_url(url)
        status = "✓" if result == expected else "✗"
        print(f"  {status} {description}: {result}")




#------------------------------------------------------------------#
#                     Test de détection de type de playlist       #
#------------------------------------------------------------------#
def test_playlist_type_detection():
    print("\n=== Test de détection de type de playlist ===")
    
    test_cases = [
        (TEST_URLS['video_simple'], "Pas une playlist"),
        (TEST_URLS['playlist_normale'], "Playlist utilisateur"),
        (TEST_URLS['playlist_radio'], "Radio/Mix automatique"),
        ("https://www.youtube.com/playlist?list=OLAK5uy_test", "Album musical"),
        ("https://www.youtube.com/playlist?list=UUtest", "Uploads de chaîne")
    ]
    
    for url, expected_type in test_cases:
        result = get_playlist_type(url)
        contains_expected = expected_type.lower() in result.lower()
        status = "✓" if contains_expected else "✗"
        print(f"  {status} {url[:40]}... -> {result}")




#------------------------------------------------------------------#
#                     Test d'affichage des informations vidéo     #
#------------------------------------------------------------------#
def test_show_video_info():
    print("\n=== Test d'affichage des informations vidéo ===")
    
    temp_dir = tempfile.mkdtemp()
    
    try:
        downloader = YouTubeDownloader(temp_dir)
        
        test_cases = [
            (TEST_URLS['video_simple'], "Vidéo simple"),
            (TEST_URLS['playlist_normale'], "Playlist normale"),
            (TEST_URLS['playlist_radio'], "Playlist radio")
        ]
        
        for url, description in test_cases:
            print(f"\nTest: {description}")
            print(f"URL: {url[:50]}...")
            
            try:
                with patch('builtins.print') as mock_print:
                    show_video_info(downloader, url)
                    
                print_calls = [str(call) for call in mock_print.call_args_list]
                if any("Informations" in call for call in print_calls):
                    print("  ✓ Informations affichées")
                else:
                    print("  ✗ Aucune information affichée")
                    
            except Exception as e:
                print(f"  ✗ Erreur: {e}")
    
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)




#------------------------------------------------------------------#
#                     Test d'affichage des formats                #
#------------------------------------------------------------------#
def test_show_available_formats():
    print("\n=== Test d'affichage des formats ===")
    
    temp_dir = tempfile.mkdtemp()
    
    try:
        downloader = YouTubeDownloader(temp_dir)
        
        test_cases = [
            (TEST_URLS['video_simple'], True, "Vidéo simple"),
            (TEST_URLS['playlist_normale'], False, "Playlist (devrait échouer)")
        ]
        
        for url, should_work, description in test_cases:
            print(f"\nTest: {description}")
            print(f"URL: {url[:50]}...")
            
            try:
                with patch('builtins.print') as mock_print:
                    show_available_formats(downloader, url)
                    
                print_calls = [str(call) for call in mock_print.call_args_list]
                
                if should_work:
                    if any("Formats disponibles" in call for call in print_calls):
                        print("  ✓ Formats affichés")
                    else:
                        print("  ✗ Formats non affichés")
                else:
                    if any("non disponible pour les playlists" in call for call in print_calls):
                        print("  ✓ Message d'erreur approprié")
                    else:
                        print("  ✗ Message d'erreur manquant")
                        
            except Exception as e:
                print(f"  ✗ Erreur: {e}")
    
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)




#------------------------------------------------------------------#
#                     Test d'affichage des vidéos de playlist     #
#------------------------------------------------------------------#
def test_show_playlist_videos():
    print("\n=== Test d'affichage des vidéos de playlist ===")
    
    temp_dir = tempfile.mkdtemp()
    
    try:
        downloader = YouTubeDownloader(temp_dir)
        
        test_cases = [
            (TEST_URLS['playlist_normale'], True, "Playlist normale"),
            (TEST_URLS['playlist_radio'], True, "Playlist radio"),
            (TEST_URLS['video_simple'], False, "Vidéo simple (devrait échouer)")
        ]
        
        for url, should_work, description in test_cases:
            print(f"\nTest: {description}")
            print(f"URL: {url[:50]}...")
            
            try:
                with patch('builtins.print') as mock_print:
                    show_playlist_videos(downloader, url)
                    
                print_calls = [str(call) for call in mock_print.call_args_list]
                
                if should_work:
                    if any("Vidéos de la playlist" in call for call in print_calls):
                        print("  ✓ Vidéos de playlist affichées")
                    elif any("Impossible de récupérer" in call for call in print_calls):
                        print("  ⚠ Playlist inaccessible (normal)")
                    else:
                        print("  ✗ Aucun affichage détecté")
                else:
                    if any("n'est pas une playlist" in call for call in print_calls):
                        print("  ✓ Message d'erreur approprié")
                    else:
                        print("  ✗ Message d'erreur manquant")
                        
            except Exception as e:
                print(f"  ✗ Erreur: {e}")
    
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)




#------------------------------------------------------------------#
#                     Test des options de ligne de commande       #
#------------------------------------------------------------------#
def test_cli_options():
    print("\n=== Test des options de ligne de commande ===")
    
    from click.testing import CliRunner
    from main.cli import main
    
    runner = CliRunner()
    
    test_cases = [
        ([TEST_URLS['video_simple'], '--info'], "Option --info"),
        ([TEST_URLS['video_simple'], '--list-formats'], "Option --list-formats"),
        ([TEST_URLS['playlist_normale'], '--list-videos'], "Option --list-videos"),
        ([TEST_URLS['video_simple'], '--quality', '720p'], "Option --quality"),
        ([TEST_URLS['video_simple'], '--audio-only'], "Option --audio-only")
    ]
    
    for args, description in test_cases:
        print(f"\nTest: {description}")
        print(f"Args: {args}")
        
        try:
            with patch('main.downloader.YouTubeDownloader') as mock_downloader:
                mock_instance = MagicMock()
                mock_downloader.return_value = mock_instance
                mock_instance.get_video_info.return_value = {
                    'title': 'Test Video',
                    'duration': 180,
                    'uploader': 'Test Channel',
                    'view_count': 1000,
                    'upload_date': '20230101'
                }
                
                result = runner.invoke(main, args)
                
                if result.exit_code == 0:
                    print("  ✓ Commande exécutée sans erreur")
                else:
                    print(f"  ✗ Erreur (code {result.exit_code}): {result.output}")
                    
        except Exception as e:
            print(f"  ✗ Exception: {e}")




#------------------------------------------------------------------#
#                     Test de gestion d'erreurs CLI              #
#------------------------------------------------------------------#
def test_cli_error_handling():
    print("\n=== Test de gestion d'erreurs CLI ===")
    
    from click.testing import CliRunner
    from main.cli import main
    
    runner = CliRunner()
    
    error_cases = [
        ([TEST_URLS['url_invalide']], "URL invalide"),
        ([""], "URL vide"),
        ([TEST_URLS['video_simple'], '--quality', 'invalid'], "Qualité invalide"),
        ([TEST_URLS['video_simple'], '--playlist-start', '-1'], "Index playlist invalide")
    ]
    
    for args, description in error_cases:
        print(f"\nTest: {description}")
        print(f"Args: {args}")
        
        try:
            result = runner.invoke(main, args)
            
            if result.exit_code != 0:
                print("  ✓ Erreur détectée et gérée")
            else:
                print("  ⚠ Commande réussie (inattendu)")
                
        except Exception as e:
            print(f"  ✓ Exception capturée: {type(e).__name__}")




#------------------------------------------------------------------#
#                     Fonction principale de test                 #
#------------------------------------------------------------------#
def run_cli_tests():
    print("YouTube Downloader - Tests CLI")
    print("=" * 50)
    
    test_url_validation()
    test_playlist_type_detection()
    test_show_video_info()
    test_show_available_formats()
    test_show_playlist_videos()
    test_cli_options()
    test_cli_error_handling()
    
    print("\n" + "=" * 50)
    print("Tests CLI terminés")




if __name__ == "__main__":
    run_cli_tests()
