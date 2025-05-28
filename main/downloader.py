import os
import yt_dlp
from pathlib import Path
from .config import DEFAULT_DOWNLOAD_PATH, QUALITY_OPTIONS, AUDIO_FORMATS, VIDEO_FORMATS, PLAYLIST_FOLDER_TEMPLATE, SINGLE_VIDEO_TEMPLATE
from .utils import create_directory, print_success, print_error, print_info, print_warning, print_progress, is_valid_youtube_url, is_playlist_url




#------------------------------------------------------------------#
#                     Classe principale de téléchargement         #
#------------------------------------------------------------------#
class YouTubeDownloader:
    def __init__(self, download_path=None):
        self.download_path = download_path or DEFAULT_DOWNLOAD_PATH
        create_directory(self.download_path)
        self.current_download = 0
        self.total_downloads = 0




    #------------------------------------------------------------------#
    #                     Télécharge une vidéo ou playlist YouTube    #
    #------------------------------------------------------------------#
    def download_video(self, url, quality="best", format_type="video", audio_only=False, playlist_start=1, playlist_end=None):
        if not is_valid_youtube_url(url):
            print_error("URL YouTube invalide")
            return False
        
        try:
            is_playlist = is_playlist_url(url)
            ydl_opts = self._get_download_options(quality, format_type, audio_only, is_playlist, playlist_start, playlist_end)
            
            if is_playlist:
                print_info("Détection d'une playlist...")
                playlist_info = self._get_playlist_info(url)
                if playlist_info:
                    print_info(f"Playlist: {playlist_info['title']}")
                    print_info(f"Nombre de vidéos: {playlist_info['video_count']}")
                    self.total_downloads = playlist_info['video_count']
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print_info(f"Téléchargement en cours...")
                ydl.download([url])
                print()
                print_success("Téléchargement terminé avec succès!")
                return True
                
        except Exception as e:
            print_error(f"Erreur lors du téléchargement: {str(e)}")
            return False




    #------------------------------------------------------------------#
    #                     Configure les options de téléchargement     #
    #------------------------------------------------------------------#
    def _get_download_options(self, quality, format_type, audio_only, is_playlist, playlist_start, playlist_end):
        quality_format = QUALITY_OPTIONS.get(quality, "best")
        
        if is_playlist:
            outtmpl = os.path.join(self.download_path, PLAYLIST_FOLDER_TEMPLATE)
        else:
            outtmpl = os.path.join(self.download_path, SINGLE_VIDEO_TEMPLATE)
        
        base_opts = {
            'outtmpl': outtmpl,
            'progress_hooks': [self._progress_hook],
        }
        
        if is_playlist:
            base_opts.update({
                'playliststart': playlist_start,
                'ignoreerrors': True,
                'extract_flat': False,
            })
            if playlist_end:
                base_opts['playlistend'] = playlist_end
        
        if audio_only:
            base_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': format_type if format_type in AUDIO_FORMATS else 'mp3',
                    'preferredquality': '192',
                }],
            })
        else:
            base_opts.update({
                'format': quality_format,
                'merge_output_format': format_type if format_type in VIDEO_FORMATS else 'mp4',
            })
        
        return base_opts




    #------------------------------------------------------------------#
    #                     Hook de progression du téléchargement       #
    #------------------------------------------------------------------#
    def _progress_hook(self, d):
        if d['status'] == 'downloading':
            if 'playlist_index' in d.get('info_dict', {}):
                current = d['info_dict']['playlist_index']
                total = d['info_dict'].get('playlist_count', self.total_downloads)
                title = d['info_dict'].get('title', '')
                print_progress(current, total, title)
        elif d['status'] == 'finished':
            if 'playlist_index' in d.get('info_dict', {}):
                print()




    #------------------------------------------------------------------#
    #                     Obtient les informations de la playlist     #
    #------------------------------------------------------------------#
    def _get_playlist_info(self, url):
        try:
            ydl_opts = {'quiet': True, 'extract_flat': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if 'entries' in info:
                    return {
                        'title': info.get('title', 'Playlist'),
                        'video_count': len(list(info['entries'])),
                        'uploader': info.get('uploader', 'N/A'),
                        'description': info.get('description', '')
                    }
        except Exception as e:
            print_error(f"Erreur lors de la récupération des informations de playlist: {str(e)}")
        return None




    #------------------------------------------------------------------#
    #                     Obtient les informations de la vidéo        #
    #------------------------------------------------------------------#
    def get_video_info(self, url):
        if not is_valid_youtube_url(url):
            return None
        
        if is_playlist_url(url):
            return self._get_playlist_info(url)
            
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




    #------------------------------------------------------------------#
    #                     Liste les formats disponibles               #
    #------------------------------------------------------------------#
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




    #------------------------------------------------------------------#
    #                     Liste les vidéos d'une playlist             #
    #------------------------------------------------------------------#
    def list_playlist_videos(self, url):
        if not is_playlist_url(url):
            print_error("L'URL n'est pas une playlist")
            return []
        
        try:
            ydl_opts = {'quiet': True, 'extract_flat': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                videos = []
                for i, entry in enumerate(info.get('entries', []), 1):
                    if entry:
                        videos.append({
                            'index': i,
                            'title': entry.get('title', 'N/A'),
                            'id': entry.get('id', 'N/A'),
                            'duration': entry.get('duration', 0),
                            'url': f"https://www.youtube.com/watch?v={entry.get('id', '')}"
                        })
                return videos
        except Exception as e:
            print_error(f"Erreur lors de la récupération de la playlist: {str(e)}")
            return []