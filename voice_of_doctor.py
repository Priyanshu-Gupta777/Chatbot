#Step 1 --> setup text to speech model (gTTS and Eleven Labs)

from gtts import gTTS

def text_to_speech(iptext, output_filepath):
    language = 'en'

    auidobj = gTTS(
        text = iptext,
        lang = language,
        slow = False,
        tld='co.in'
    )

    auidobj.save(output_filepath)

#iptext = "Hi There! My name is Google"
#output_filepath = 'gtts_testing.mp3'

#text_to_speech(iptext,output_filepath)




#Step 2 --> Use model text to output voice

import os
import platform
import subprocess
from gtts import gTTS
from pydub import AudioSegment

AudioSegment.converter = "/usr/bin/ffmpeg"
AudioSegment.ffmpeg = "/usr/bin/ffmpeg"
AudioSegment.ffprobe = "/usr/bin/ffprobe"

def text_to_speech_auto(inptext, output_file):
    language = 'en'

    audio_obj = gTTS(
        text = inptext,
        lang = language,
        slow = False,
        tld='co.in'
    )

    mp3_file = output_file
    wav_file = output_file.replace('.mp3', '.wav')  # Convert to WAV

    audio_obj.save(mp3_file)  # Save as MP3

   
    sound = AudioSegment.from_mp3(mp3_file)
    sound.export(wav_file, format="wav")  

    # Detect OS and play the WAV file
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', wav_file])
        elif os_name == "Windows":  # Windows
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{wav_file}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', wav_file])  # Alternative: 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

#inptext = "Hi There! My name is Autoplay"
#output_file = 'gtts_autotesting.mp3'

#text_to_speech_auto(inptext,output_file)