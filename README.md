# YouTube Downloader

Un utilitaire simple et efficace pour télécharger des vidéos YouTube avec choix de qualité et répertoire personnalisable.

## Installation

### Installation depuis les sources

```bash
git clone https://github.com/henocn/youtube-downloader.git
cd youtube-downloader
pip install -r requirements.txt
pip install -e .
```

### Installation des dépendances uniquement

```bash
pip install yt-dlp click colorama
```

## Utilisation

### Commande de base

```bash
yt-download "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Options disponibles

| Option | Raccourci | Description | Défaut |
|--------|-----------|-------------|---------|
| `--quality` | `-q` | Qualité vidéo (worst, 360p, 480p, 720p, 1080p, 1440p, 2160p, best) | best |
| `--output` | `-o` | Répertoire de téléchargement | ~/Downloads/youtube-downloads |
| `--audio-only` | `-a` | Télécharger uniquement l'audio | False |
| `--format` | `-f` | Format de sortie | mp4 |
| `--info` | `-i` | Afficher les informations sans télécharger | False |
| `--list-formats` | `-l` | Lister tous les formats disponibles | False |

### Exemples d'utilisation

#### Téléchargement basique
```bash
yt-download "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

#### Téléchargement en 720p dans un dossier spécifique
```bash
yt-download "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -q 720p -o "/path/to/downloads"
```

#### Téléchargement audio uniquement en MP3
```bash
yt-download "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -a -f mp3
```

#### Afficher les informations de la vidéo
```bash
yt-download "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -i
```

#### Lister les formats disponibles
```bash
yt-download "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -l
```

#### Téléchargement en format WebM
```bash
yt-download "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -f webm -q 1080p
```

## Formats supportés

### Vidéo
- mp4 (défaut)
- webm
- mkv
- avi

### Audio
- mp3 (défaut)
- m4a
- wav
- aac

## Qualités disponibles

- `worst` : Plus basse qualité disponible
- `360p` : 360p maximum
- `480p` : 480p maximum
- `720p` : 720p maximum (HD)
- `1080p` : 1080p maximum (Full HD)
- `1440p` : 1440p maximum (2K)
- `2160p` : 2160p maximum (4K)
- `best` : Meilleure qualité disponible (défaut)

## Utilisation en tant que module Python

```python
from main import YouTubeDownloader

downloader = YouTubeDownloader("/path/to/downloads")

# Téléchargement vidéo
downloader.download_video("https://www.youtube.com/watch?v=VIDEO_ID", quality="720p")

# Téléchargement audio uniquement
downloader.download_video("https://www.youtube.com/watch?v=VIDEO_ID", audio_only=True, format_type="mp3")

# Obtenir les informations
info = downloader.get_video_info("https://www.youtube.com/watch?v=VIDEO_ID")
print(info)
```

## Prérequis

- Python 3.8+
- FFmpeg (pour la conversion audio)

### Installation de FFmpeg

#### Windows
Télécharger depuis [ffmpeg.org](https://ffmpeg.org/download.html) et ajouter au PATH

#### macOS
```bash
brew install ffmpeg
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install ffmpeg
```

## Dépannage

### Erreur "FFmpeg not found"
Assurez-vous que FFmpeg est installé et accessible dans votre PATH.

### Erreur de permissions
Vérifiez que vous avez les droits d'écriture dans le répertoire de destination.

### Vidéo non disponible
Certaines vidéos peuvent être géo-bloquées ou privées.

## Licence

MIT License - voir le fichier LICENSE pour plus de détails.

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou soumettre une pull request.
```

## 9. Instructions d'installation et d'utilisation

### Script d'installation automatique

```batch:install.bat
@echo off
echo Installation de YouTube Downloader...
echo.

echo 1. Installation des dependances...
pip install yt-dlp click colorama

echo.
echo 2. Installation du package...
pip install -e .

echo.
echo 3. Test de l'installation...
yt-download --help

echo.
echo Installation terminee!
echo Vous pouvez maintenant utiliser la commande: yt-download
pause
```

### Script de test

```batch:test.bat
@echo off
echo Test de YouTube Downloader...
echo.

echo Test 1: Affichage de l'aide
yt-download --help
echo.

echo Test 2: Informations d'une video (sans telechargement)
set /p url="Entrez une URL YouTube pour tester: "
yt-download "%url%" -i

echo.
echo Tests termines!
pause
```

### Commandes d'installation manuelle

```bash
cd youtube-downloader
```

```bash
pip install -r requirements.txt
```

```bash
pip install -e .
```

```bash
yt-download --help
```

### Exemple d'utilisation complète

```bash
yt-download "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -q 720p -o "C:\Downloads\YouTube" -f mp4
