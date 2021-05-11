import speech_recognition as sr
from dependencies.handlers._ffmpeg import chop_chop, format_to_ffmpeg_duration


def get_audio_transcript(path_to_file, recognizer: sr.Recognizer):
    with sr.AudioFile(path_to_file) as source:
        return recognizer.recognize_google(recognizer.record(source))

def gat_with_breakdown(path_to_file, recognizer: sr.Recognizer, breakdown_duration=10, tempfile_name='temp.wav'):
    """
    gat = get audio transcript
    
    This breakdown is effective for writing down SRT(s).
    """
    for start, end, total in chop_chop(path_to_file, breakdown_duration, output_file=tempfile_name):
        last_yield = start
        with sr.AudioFile(tempfile_name) as source:
            try:
                if (content := recognizer.recognize_google(recognizer.record(source))):
                    yield {'start': format_to_ffmpeg_duration(start), 'end': format_to_ffmpeg_duration(end), 'text': content, 'total': total, 'delta': end - last_yield}
                    last_yield = end
            except sr.UnknownValueError:
                pass
