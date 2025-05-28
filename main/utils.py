#------------------------------------------------------------------#
#                     Fonctions utilitaires                       #
#------------------------------------------------------------------#
import os
import re
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import colorama
from colorama import Fore, Style

colorama.init()




#------------------------------------------------------------------#
#                     Valide une URL YouTube                      #
#------------------------------------------------------------------#
def is_valid_youtube_url(url):
    youtube_regex = re.compile(
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    playlist_regex = re.compile(
        r'(https?://)?(www\.)?youtube\.com/(playlist\?list=|watch\?.*list=)([a-zA-Z0-9_-]+)'
    )
    return youtube_regex.match(url) is not None or playlist_regex.match(url) is not None




#------------------------------------------------------------------#
#                     Vérifie si l'URL est une playlist           #
#------------------------------------------------------------------#
def is_playlist_url(url):
    return "list=" in url and ("playlist?" in url or "watch?" in url)




#------------------------------------------------------------------#
#                     Extrait l'ID de la playlist                 #
#------------------------------------------------------------------#
def extract_playlist_id(url):
    if "list=" in url:
        return url.split("list=")[1].split("&")[0]
    return None




#------------------------------------------------------------------#
#                     Extrait l'ID de la vidéo                    #
#------------------------------------------------------------------#
def extract_video_id(url):
    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    elif "watch?v=" in url:
        return url.split("watch?v=")[1].split("&")[0]
    return None




#------------------------------------------------------------------#
#                     Crée un répertoire s'il n'existe pas        #
#------------------------------------------------------------------#
def create_directory(path):
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print_error(f"Erreur lors de la création du répertoire: {e}")
        return False




#------------------------------------------------------------------#
#                     Affiche un message de succès               #
#------------------------------------------------------------------#
def print_success(message):
    print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")




#------------------------------------------------------------------#
#                     Affiche un message d'erreur                #
#------------------------------------------------------------------#
def print_error(message):
    print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")




#------------------------------------------------------------------#
#                     Affiche un message d'information           #
#------------------------------------------------------------------#
def print_info(message):
    print(f"{Fore.BLUE}ℹ {message}{Style.RESET_ALL}")




#------------------------------------------------------------------#
#                     Affiche un message d'avertissement         #
#------------------------------------------------------------------#
def print_warning(message):
    print(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")




#------------------------------------------------------------------#
#                     Affiche la progression                      #
#------------------------------------------------------------------#
def print_progress(current, total, title=""):
    percentage = (current / total) * 100
    bar_length = 30
    filled_length = int(bar_length * current // total)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    print(f"\r{Fore.CYAN}[{bar}] {percentage:.1f}% ({current}/{total}) {title[:50]}{Style.RESET_ALL}", end='', flush=True)
