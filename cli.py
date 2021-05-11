import os

from tqdm import tqdm

from core.filec import get_temporary_file
from core.listener import gat_with_breakdown, sr

SRT_TEMPLATE = """\
{index}
{start} --> {end}
{text}

"""

def __cli_caller__():
    
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Path to the audio/video file for subtitle generation.", required=True)
    parser.add_argument("-o", "--output", help="Path for the output '.SRT' file.", default='subtitles.srt')
    parser.add_argument("-t", "--temp-file", help="Path for the temporary files that are going to be formed during subtitle generation.", default='temp.wav')
    parser.add_argument("-d", "--duration", help="A duration (time interval) acting as separations for your subtitles.", default=5, type=int)
    parser.add_argument("-q", "--quiet", help="Quiet mode, 1 for activation, anything else for deactivation.", default=0, type=int)
    
    arguments = parser.parse_args()
    
    real_input = get_temporary_file(arguments.input, "t2.wav", quiet=(quiet := bool(arguments.quiet)))

    with open(arguments.output, 'w') as srt_file:
        if not quiet:
            progress_bar = None
        
        for n, data in enumerate(gat_with_breakdown(real_input, sr.Recognizer(), arguments.duration, arguments.temp_file), 1):
            if not quiet:
                if not progress_bar:
                    progress_bar = tqdm(desc='Generating subtitles: ', total=data.get('total').total_seconds(), unit='s')

                progress_bar.update(data.get('delta').total_seconds())
            
            srt_file.write(SRT_TEMPLATE.format(index=n, **data))
    
    if not quiet:
        progress_bar.close()
            
    if not real_input == arguments.input:
        os.remove(real_input)
    
    print("Successfully generated subtitles to %s." % arguments.output)
    
if __name__ == '__main__':
    __cli_caller__()
