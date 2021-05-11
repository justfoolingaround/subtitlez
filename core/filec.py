"""
An effective converter that would basically just convert YouTube videos and/or URL(s) to files for subtitle generation.
"""

import re

import requests
from tqdm import tqdm
from youtube_dl import YoutubeDL

from dependencies.handlers._ffmpeg import get_audio, ensure_inexistence

YT_RE = re.compile(r'^(?:https?://)?(?:www\.)?youtu(?:\.be/|be.com/\S*(?:watch|embed)(?:(?:(?=\/[^&\s\?]+(?!\S))/)|(?:\S*v=|v/)))([^&\s\?]+)')
URL_RE = re.compile(r"\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")

ytdl = YoutubeDL({'format':'webm[abr>0]/bestaudio/best', 'prefer_ffmpeg': True, 'quiet':True})

def download(url, filename, session=None, headers={}, quiet=False):
    """
    Just a downloader yoinked from old code(s).
    """
    session = session or requests.Session()
    
    content_header = session.head(url, headers=headers).headers
    
    r = int(content_header.get('content-length', 0) or 0)    
    d = 0
    
    assert r, "The file is not downloadable!"
    
    if not quiet:
        tqdm_bar = tqdm(desc="Downloading file to %s: " % filename, total=r, unit='B', unit_scale=True)
    
    with open(filename, 'ab') as sw:
        d = sw.tell()
        if not quiet:
            tqdm_bar.update(d)
        while r > d:
            try:
                for chunks in requests.get(url, stream=True, headers={'Range': 'bytes=%d-' % d} | headers,).iter_content(0x4000):
                    size = len(chunks)
                    d += size
                    if not quiet:
                        tqdm_bar.update(size)
                    sw.write(chunks)
            except requests.RequestException:
                pass
            
    if not quiet:
        tqdm_bar.close()
    
def extract_audio_file(path_to_file, temp_file_path, quiet, *, delete=True):
    if not quiet:
        print("Converting %s to recognizable format forehand." % path_to_file)
    get_audio(path_to_file, output_file=temp_file_path)
    if delete:
        ensure_inexistence(path_to_file)
    return temp_file_path

def get_temporary_file(input_file: str, temp_file_path: str, quiet=False):
    
    if YT_RE.match(input_file):
        download(ytdl.extract_info(input_file, download=False).get('url'), "yt.webm", quiet=quiet)
        return extract_audio_file('yt.webm', temp_file_path, quiet=quiet)
    
    if URL_RE.match(input_file):
        download(input_file, "url.webm", quiet=quiet)
        return extract_audio_file('url.webm', temp_file_path, quiet=quiet)
        
    if not input_file.endswith(('.wav', '.flac')):
        return extract_audio_file(input_file, temp_file_path, quiet=quiet, delete=False)
    
    return input_file