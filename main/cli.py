import click
import os
from .downloader import YouTubeDownloader
from .config import QUALITY_OPTIONS, AUDIO_FORMATS, VIDEO_FORMATS, DEFAULT_DOWNLOAD_PATH
from .utils import print_success, print_error, print_info, print_warning, is_playlist_url




#------------------------------------------------------------------#
#                     Commande principale CLI                     #
#------------------------------------------------------------------#
@click.command()
@click.argument('url')
@click.option('--quality', '-q', default='best', 
              type=click.Choice(list(QUALITY_OPTIONS.keys())), 
              help='Qualité de la vidéo')
@click.option('--output', '-o', default=DEFAULT_DOWNLOAD_PATH, 
              help='Répertoire de téléchargement')
@click.option('--audio-only', '-a', is_flag=True, 
              help='Télécharger uniquement l\'audio')
@click.option('--format', '-f', default='mp4', 
              help='Format de sortie (mp4, webm, mkv pour vidéo | mp3, m4a, wav pour audio)')
@click.option('--info', '-i', is_flag=True, 
              help='Afficher les informations de la vidéo/playlist sans télécharger')
@click.option('--list-formats', '-l', is_flag=True, 
              help='Lister tous les formats disponibles')
@click.option('--playlist-start', '-ps', default=1, type=int,
              help='Index de début pour les playlists (défaut: 1)')
@click.option('--playlist-end', '-pe', type=int,
              help='Index de fin pour les playlists (optionnel)')
@click.option('--list-videos', '-lv', is_flag=True,
              help='Lister toutes les vidéos d\'une playlist')
def main(url, quality, output, audio_only, format, info, list_formats, playlist_start, playlist_end, list_videos):
    print_info("YouTube Downloader v1.0.0")
    print_info(f"URL: {url}")
    
    downloader = YouTubeDownloader(output)
    
    if info:
        show_video_info(downloader, url)
        return
    
    if list_formats:
        show_available_formats(downloader, url)
        return
    
    if list_videos:
        show_playlist_videos(downloader, url)
        return
    
    if audio_only and format not in AUDIO_FORMATS:
        print_warning(f"Format {format} non supporté pour l'audio, utilisation de mp3")
        format = 'mp3'
    elif not audio_only and format not in VIDEO_FORMATS:
        print_warning(f"Format {format} non supporté pour la vidéo, utilisation de mp4")
        format = 'mp4'
    
    if is_playlist_url(url):
        print_info("=== TÉLÉCHARGEMENT DE PLAYLIST ===")
        if playlist_end:
            print_info(f"Plage: vidéos {playlist_start} à {playlist_end}")
        else:
            print_info(f"Début: vidéo {playlist_start}")
    
    print_info(f"Qualité: {quality}")
    print_info(f"Format: {format}")
    print_info(f"Audio seulement: {'Oui' if audio_only else 'Non'}")
    print_info(f"Répertoire: {output}")
    
    success = downloader.download_video(url, quality, format, audio_only, playlist_start, playlist_end)
    if success:
        print_success(f"Fichier(s) sauvegardé(s) dans: {output}")
    else:
        print_error("Échec du téléchargement")




#------------------------------------------------------------------#
#                     Affiche les informations de la vidéo/playlist #
#------------------------------------------------------------------#
def show_video_info(downloader, url):
    info = downloader.get_video_info(url)
    if info:
        if is_playlist_url(url):
            print_info("=== Informations de la playlist ===")
            print(f"Titre: {info['title']}")
            print(f"Nombre de vidéos: {info['video_count']}")
            print(f"Auteur: {info['uploader']}")
            if info.get('description'):
                print(f"Description: {info['description'][:100]}...")
        else:
            print_info("=== Informations de la vidéo ===")
            print(f"Titre: {info['title']}")
            print(f"Durée: {info['duration']} secondes")
            print(f"Auteur: {info['uploader']}")
            print(f"Vues: {info['view_count']:,}")
            print(f"Date: {info['upload_date']}")
    else:
        print_error("Impossible de récupérer les informations")




#------------------------------------------------------------------#
#                     Affiche les formats disponibles             #
#------------------------------------------------------------------#
def show_available_formats(downloader, url):
    if is_playlist_url(url):
        print_warning("Affichage des formats non disponible pour les playlists")
        print_info("Utilisez une URL de vidéo individuelle")
        return
    
    formats = downloader.list_formats(url)
    if formats:
        print_info("=== Formats disponibles ===")
        for fmt in formats[:10]:
            resolution = fmt.get('resolution', 'N/A')
            ext = fmt.get('ext', 'N/A')
            filesize = fmt.get('filesize', 0)
            size_mb = f"{filesize/1024/1024:.1f}MB" if filesize else "N/A"
            print(f"Format: {ext} | Résolution: {resolution} | Taille: {size_mb}")
    else:
        print_error("Impossible de récupérer les formats")




#------------------------------------------------------------------#
#                     Affiche les vidéos d'une playlist           #
#------------------------------------------------------------------#
def show_playlist_videos(downloader, url):
    if not is_playlist_url(url):
        print_error("L'URL fournie n'est pas une playlist")
        return
    
    videos = downloader.list_playlist_videos(url)
    if videos:
        print_info(f"=== Vidéos de la playlist ({len(videos)} vidéos) ===")
        for video in videos:
            duration_str = f"{video['duration']//60}:{video['duration']%60:02d}" if video['duration'] else "N/A"
            print(f"{video['index']:2d}. {video['title']} ({duration_str})")
            if len(videos) > 20 and video['index'] == 20:
                remaining = len(videos) - 20
                print(f"    ... et {remaining} autres vidéos")
                break
    else:
        print_error("Impossible de récupérer la liste des vidéos")




if __name__ == '__main__':
    main()