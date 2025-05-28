#------------------------------------------------------------------#
#                     Package youtube downloader                  #
#------------------------------------------------------------------#
__version__ = "1.0.0"
__author__ = "Henoc N'GASAMA"
__description__ = "Simple YouTube video downloader"

from .downloader import YouTubeDownloader
from .cli import main

__all__ = ['YouTubeDownloader', 'main']
