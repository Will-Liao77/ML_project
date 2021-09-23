import tempfile
from pygame import mixer
from gtts import gTTS


def speak(sentence, lang):
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts = gTTS(text=sentence, lang=lang)
        tts.save('{}.mp3'.format(fp.name))
        mixer.init()
        mixer.music.load('{}.mp3'.format(fp.name))
        mixer.music.play(1)


speak('Hello World!', 'en')
