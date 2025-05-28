import click
import os
from .downloader import YouTubeDownloader
from .config import QUALITY_OPTIONS, AUDIO_FORMATS, VIDEO_FORMATS, DEFAULT_DOWNLOAD_PATH
from .utils import print_success, print_error, print_info, print_warning




#------------------------------------------------------------------#
#                     Commande principale CLI                      #
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
              help='Afficher les informations de la vidéo sans télécharger')
@click.option('--list-formats', '-l', is_flag=True, 
              help='Lister tous les formats disponibles')
def main(url, quality, output, audio_only, format, info, list_formats):
    print_info("YouTube Downloader v1.0.0")
    print_info(f"URL: {url}")
    
    downloader = YouTubeDownloader(output)
    
    if info:
        show_video_info(downloader, url)
        return
    
    if list_formats:
        show_available_formats(downloader, url)
        return
    
    if audio_only and format not in AUDIO_FORMATS:
        print_warning(f"Format {format} non supporté pour l'audio, utilisation de mp3")
        format = 'mp3'
    elif not audio_only and format not in VIDEO_FORMATS:
        print_warning(f"Format {format} non supporté pour la vidéo, utilisation de mp4")
        format = 'mp4'
    
    print_info(f"Qualité: {quality}")
    print_info(f"Format: {format}")
    print_info(f"Audio seulement: {'Oui' if audio_only else 'Non'}")
    print_info(f"Répertoire: {output}")
    
    success = downloader.download_video(url, quality, format, audio_only)
    if success:
        print_success(f"Fichier sauvegardé dans: {output}")
    else:
        print_error("Échec du téléchargement")




#------------------------------------------------------------------#
#                 Affiche les informations de la vidéo             #
#------------------------------------------------------------------#
def show_video_info(downloader, url):
    info = downloader.get_video_info(url)
    if info:
        print_info("=== Informations de la vidéo ===")
        print(f"Titre: {info['title']}")
        print(f"Durée: {info['duration']} secondes")
        print(f"Auteur: {info['uploader']}")
        print(f"Vues: {info['view_count']:,}")
        print(f"Date: {info['upload_date']}")
    else:
        print_error("Impossible de récupérer les informations")




#------------------------------------------------------------------#
#                  Affiche les formats disponibles                 #
#------------------------------------------------------------------#
def show_available_formats(downloader, url):
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




if __name__ == '__main__':
    main()
