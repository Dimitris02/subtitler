import speech_recognition as sr 
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence, detect_nonsilent
from moviepy.editor import *
import deepl_scraper as ds

r = sr.Recognizer()

LANG='ru-RU'            # More languages at https://cloud.google.com/speech-to-text/docs/speech-to-text-supported-languages
TRANSLATE_TO=''         # Pick language to translate to. Leaving it empty will default to the language of your IP address
SILENCE=500             # Reduce if the dialog is continuous with few pauses
THRESH=10               # Reduce if the speech-to-noise ratio is low

def vid2sub(v):
    a = v[:v.rfind(".")]
    return a+"_ORIGINAL.srt"

def timestamp(mseconds):
    (hours, mseconds) = divmod(mseconds, 3600000)
    (minutes, mseconds) = divmod(mseconds, 60000)
    (seconds, mseconds) = divmod(mseconds, 1000)
    return f"{hours:02.0f}:{minutes:02.0f}:{seconds:02.0f},{mseconds:03.0f}"

def formt(ms):
    ms=max(0,ms)
    return timestamp(ms)

def add_quote(num, start, end, quote):
    return str(num) + "\n" + formt(start) + " --> " + formt(end) + "\n" + quote + "\n\n"

def transcribe_audio(path):
    with sr.AudioFile(path) as source:
        audio_listened = r.record(source)
        text = r.recognize_google(audio_listened, language=LANG)
    return text

def capture_audio(vid):

    VideoFileClip(vid).audio.write_audiofile("tmp.wav")
    print("Analyzing audio...")
    sound = AudioSegment.from_file("tmp.wav", format="wav")
    nd = detect_nonsilent(sound, min_silence_len=SILENCE, silence_thresh=sound.dBFS-THRESH, seek_step=1)

    chunks = split_on_silence(sound, min_silence_len = SILENCE, silence_thresh = sound.dBFS-THRESH, keep_silence=SILENCE)
    whole_text = ""

    for i, audio_chunk in enumerate(chunks, start=1):

        chunk_filename = "chunk.wav"
        audio_chunk.export(chunk_filename, format="wav")

        try:
            text = transcribe_audio(chunk_filename)
        except sr.UnknownValueError as e:
            print("Error:", str(e))
        else:
            text = f"{text.capitalize()}. "
            print(chunk_filename, ":", text)
            whole_text += add_quote(i, nd[i-1][0]-250, nd[i-1][1]+500, text)

    os.remove(chunk_filename) 
    os.remove("tmp.wav") 
    with open(vid2sub(vid), "wb") as f:
        f.write(whole_text.encode('utf8'))
    
def main(file):
    capture_audio(file)
    ds.translate(vid2sub(file), file, TRANSLATE_TO)

if __name__ == "__main__":
    while True:
        os.system("cls")
        print("Subtitler v1.0.0\n")
        print("(Type in \"help\" for a list of commands)\n")
        print("LANG:            "+LANG)
        print("TRANSLATE_TO:    "+TRANSLATE_TO)
        print("SILENCE:         "+str(SILENCE))
        print("THRESH:          "+str(THRESH))
        print("")
        f=input(">").split()
        if f[0].lower()=="lang":
            LANG=f[1]
        elif f[0].lower()=="translate_to":
            TRANSLATE_TO=f[1]
        elif f[0].lower()=="silence":
            SILENCE=f[1]
        elif f[0].lower()=="thresh":
            THRESH=f[1]
        elif f[0].lower()=="help":
            print("\nlang <BCP-47>: Pick a language to translate from. More languages at https://cloud.google.com/speech-to-text/docs/speech-to-text-supported-languages\n")
            print("translate_to <language>: Pick a language to translate to.\n")
            print("silence <int>: Reduce if the dialog is continuous with few pauses\n")
            print("thresh <int>: Reduce if the speech-to-noise ratio is low\n")
            print("Anything else typed will be interpreted as a video filename to add subtitles to.\n")
            os.system('pause')
        else:
            main(f[0])
