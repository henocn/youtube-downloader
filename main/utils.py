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
#                     Valide une URL YouTube                       #
#------------------------------------------------------------------#
def is_valid_youtube_url(url):
    youtube_regex = re.compile(
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    return youtube_regex.match(url) is not None




#------------------------------------------------------------------#
#                     Extrait l'ID de la vidéo                     #
#------------------------------------------------------------------#
def extract_video_id(url):
    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    elif "watch?v=" in url:
        return url.split("watch?v=")[1].split("&")[0]
    return None




#------------------------------------------------------------------#
#                     Crée un répertoire s'il n'existe pas         #
#------------------------------------------------------------------#
def create_directory(path):
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print_error(f"Erreur lors de la création du répertoire: {e}")
        return False




#------------------------------------------------------------------#
#                     Affiche un message de succès                 #
#------------------------------------------------------------------#
def print_success(message):
    print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")




#------------------------------------------------------------------#
#                     Affiche un message d'erreur                  #
#------------------------------------------------------------------#
def print_error(message):
    print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")




#------------------------------------------------------------------#
#                     Affiche un message d'information             #
#------------------------------------------------------------------#
def print_info(message):
    print(f"{Fore.BLUE}ℹ {message}{Style.RESET_ALL}")




#------------------------------------------------------------------#
#                     Affiche un message d'avertissement           #
#------------------------------------------------------------------#
def print_warning(message):
    print(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")
