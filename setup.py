from setuptools import setup, find_packages
import os

def safe_read(filename, default=""):
    if not os.path.exists(filename):
        return default
    
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as f:
                content = f.read()
                if content.startswith('\ufeff'):
                    content = content[1:]
                return content
        except (UnicodeDecodeError, UnicodeError):
            continue
    
    return default

REQUIREMENTS = [
    "click==8.2.1",
    "colorama==0.4.6", 
    "yt-dlp==2025.5.22",
]

long_description = safe_read("README.md", "YouTube Downloader - Un téléchargeur YouTube simple et efficace")

setup(
    name="youtube-downloader",
    version="1.0.0",
    author="Henoc N'GASAMA",
    author_email="ngasamah@gmail.com",
    description="Un téléchargeur YouTube simple et efficace",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/henocn/youtube-downloader",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Video",
        "Topic :: Internet :: WWW/HTTP",
    ],
    python_requires=">=3.8",
    install_requires=REQUIREMENTS,
    entry_points={
        "console_scripts": [
            "yt-download=main.cli:main",
        ],
    },
    include_package_data=True,
)
