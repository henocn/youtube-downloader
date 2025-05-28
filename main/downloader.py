import os
import yt_dlp
from pathlib import Path
from .config import DEFAULT_DOWNLOAD_PATH, QUALITY_OPTIONS, AUDIO_FORMATS, VIDEO_FORMATS
from .utils import create_directory, print_success, print_error, print_info, is_valid_youtube_url




#------------------------------------------------------------------#
#                 Classe principale de téléchargement              #
#------------------------------------------------------------------#
class YouTubeDownloader:
    def __init__(self, download_path=None):
        self.download_path = download_path or DEFAULT_DOWNLOAD_PATH
        create_directory(self.download_path)


    #élécharge une vidéo YouTube
    def download_video(self, url, quality="best", format_type="video", audio_only=False):
        if not is_valid_youtube_url(url):
            print_error("URL YouTube invalide")
            return False
        
        try:
            ydl_opts = self._get_download_options(quality, format_type, audio_only)
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print_info(f"Téléchargement en cours...")
                ydl.download([url])
                print_success("Téléchargement terminé avec succès!")
                return True
                
        except Exception as e:
            print_error(f"Erreur lors du téléchargement: {str(e)}")
            return False


    #Configure les options de téléchargement
    def _get_download_options(self, quality, format_type, audio_only):
        quality_format = QUALITY_OPTIONS.get(quality, "best")
        
        if audio_only:
            outtmpl = os.path.join(self.download_path, '%(title)s.%(ext)s')
            return {
                'format': 'bestaudio/best',
                'outtmpl': outtmpl,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': format_type if format_type in AUDIO_FORMATS else 'mp3',
                    'preferredquality': '192',
                }],
            }
        else:
            outtmpl = os.path.join(self.download_path, '%(title)s.%(ext)s')
            return {
                'format': quality_format,
                'outtmpl': outtmpl,
                'merge_output_format': format_type if format_type in VIDEO_FORMATS else 'mp4',
            }


    #Obtient les informations de la vidéo
    def get_video_info(self, url):
        if not is_valid_youtube_url(url):
            return None
            
        try:
            ydl_opts = {'quiet': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', 'N/A'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'N/A'),
                    'view_count': info.get('view_count', 0),
                    'upload_date': info.get('upload_date', 'N/A')
                }
        except Exception as e:
            print_error(f"Erreur lors de la récupération des informations: {str(e)}")
            return None


    #Liste les formats disponibles
    def list_formats(self, url):
        if not is_valid_youtube_url(url):
            return []
            
        try:
            ydl_opts = {'quiet': True, 'listformats': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info.get('formats', [])
        except Exception as e:
            print_error(f"Erreur lors de la récupération des formats: {str(e)}")
            return []
