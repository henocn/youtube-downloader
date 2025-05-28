#------------------------------------------------------------------#
#                     Configuration par défaut                    #
#------------------------------------------------------------------#
import os
from pathlib import Path

DEFAULT_DOWNLOAD_PATH = os.path.join(str(Path.home()), "Downloads", "youtube-downloads")
DEFAULT_QUALITY = "best"

QUALITY_OPTIONS = {
    "worst": "worst",
    "360p": "best[height<=360]",
    "480p": "best[height<=480]", 
    "720p": "best[height<=720]",
    "1080p": "best[height<=1080]",
    "1440p": "best[height<=1440]",
    "2160p": "best[height<=2160]",
    "best": "best"
}

AUDIO_FORMATS = ["mp3", "m4a", "wav", "aac"]
VIDEO_FORMATS = ["mp4", "webm", "mkv", "avi"]

PLAYLIST_FOLDER_TEMPLATE = "%(playlist_title)s/%(playlist_index)02d - %(title)s.%(ext)s"
SINGLE_VIDEO_TEMPLATE = "%(title)s.%(ext)s"