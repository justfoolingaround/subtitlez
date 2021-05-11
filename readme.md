Subtitlez
---

Subtitlez is a simple yet, powerful program to generate subtitle(s) in the most standard `srt` format for your videos and/or music file(s).

**Arguments**

There are a few arguments that will make your experience with this program significantly easier.

| Argument | Description | 
| -------- | ----------- | 
| -i/--input | A required argument to point towards the target file. This can be a YouTube URL or a URL to a video file. |
| -o/--output | An optional argument for setting a custom output file. By default, this is set to `subtitles.srt` |
| -t/--temp-file | An optional argument for setting a custom name for the temporary file that would be generated throughout the subtitle generation. This file will be deleted after the subtitles generate. |
| -d/--duration | An optional argument for setting the interval of audio that is to be sent for recognition. If this is set to 5, each 5 seconds of the audio file will be sent for recognition. |
| -q/--quiet | An optional argument for making all the progress bar / stdout gibberish go away. |
| -h/--help | And this would be for showing a poorly written help. |

**Disclaimer**

This program is slow and not at all reliable for *most* use cases (it is only created to mess around with automation and Google APIs). You might want to use this program if you want to generate a general template of your subtitle file.

**External Dependencies**

For the execution of this program, you will have to download `ffmpeg` to the PATH or to the working directory.

**TODO(s)**

Well, the main TODO for this program is to add features which contain additional audio data analysis functions that would help to recognize the audio accurately. These functions will most probably be able to locate vocals for further recognition.