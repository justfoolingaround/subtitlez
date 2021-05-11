"""
ffmpeg handlers; strictly for Windows.
"""

import os
import re
import shutil
import subprocess
from datetime import timedelta

has_ffmpeg = lambda dependency_name='ffmpeg': bool(shutil.which(dependency_name))

def ensure_inexistence(file):    
    from pathlib import Path
    
    if (p := Path('.') / Path(file)).is_file():
        os.remove(p)


def do_after(f, timeout=0):
    """
    A scheduler.
    """
    import threading
    import time
    
    return threading.Thread(target=lambda: time.sleep(timeout) or f()).start()

def ensure_ffmpeg(f):
    def inner(*args, **kwargs):
        if not has_ffmpeg():
            raise Exception('ffmpeg is was not found in the PATH or the working directory.')
        return f(*args, **kwargs)
    return inner

@ensure_ffmpeg
def ffmpeg_call(arguments):
    return (caller := subprocess.run(['ffmpeg', *arguments], capture_output=True, text=True, timeout=10)).stderr or caller.stdout

ffmpeg_call_grab = ensure_ffmpeg(lambda arguments, regexp, *, flags=re.M: re.search(regexp, ffmpeg_call(arguments), flags=flags))

@ensure_ffmpeg
def is_latest(*, session=None, version_info_uri="https://www.gyan.dev/ffmpeg/builds/release-version"):
    """
    Check if the version available in the device is the latest version of ffmpeg.
    """
    import requests
    
    return re.match(r"^ffmpeg version ([\d\.]+)", subprocess.run(['ffmpeg'], capture_output=True, text=True).stderr).group(1) == (session or requests.Session()).get(version_info_uri).text

@ensure_ffmpeg
def get_audio(path_to_file, *, output_file='temp.mp3', additional_commands=[]):
    """
    All the video to audio "converter(s)" in the world in 3 lines.
    """
    ensure_inexistence(output_file)
    
    ffmpeg_call(['-i', path_to_file, '-vn', output_file] + additional_commands)
    return output_file
    
parse_duration = lambda duration: timedelta(**{t: float(v) for t, v in re.search(r"(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>[\d\.]+)", duration).groupdict().items()})

def format_to_ffmpeg_duration(td_obj: timedelta):
    hours, rem = divmod(td_obj.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    return "{:02d}:{:02d}:{:02d}.{}".format(hours, minutes, seconds, td_obj.microseconds)

@ensure_ffmpeg
def chop_chop(path_to_file, chopping_duration=3.0, *, output_file='temp.mp3', additional_commands=[]):
    """
    Chop chop is a generator that would chop an audio file into pieces with ffmpeg calls.
    """
    ensure_inexistence(output_file)
    
    duration = parse_duration(ffmpeg_call_grab(['-i', path_to_file], r"Duration: ([\d:\.]+)").group(1))
    current = timedelta()
    while current - timedelta(seconds=chopping_duration) < duration:
        ffmpeg_call(['-i', path_to_file, '-acodec', 'copy', '-ss', format_to_ffmpeg_duration(current), '-to', format_to_ffmpeg_duration(current := (current + timedelta(seconds=chopping_duration))), output_file] + additional_commands)
        yield current - timedelta(seconds=chopping_duration), current, duration
        os.remove(output_file)