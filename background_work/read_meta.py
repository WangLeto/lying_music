import os
import wave
import contextlib
from mutagen.flac import FLAC
from mutagen.monkeysaudio import MonkeysAudio
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4

valid_list = ['.mp3', '.m4a', '.flac', '.ape']


def read_meta(_path):
    ex_name = os.path.splitext(_path)[-1]
    try:
        if ex_name == '.mp3':
            audio = MP3(_path)
            artist = str(audio.tags.getall('TPE1')[0])
            title = str(audio.tags.getall('TIT2')[0])
        elif ex_name == '.m4a':
            audio = MP4(_path)
            title = str(audio.tags['\xa9nam'][0])
            artist = str(audio.tags['\xa9ART'][0])
        elif ex_name == '.flac':
            audio = FLAC(_path)
            title = audio['title'][0]
            artist = audio['artist'][0]
        else:
            audio = MonkeysAudio(_path)
            title = str(audio['title'])
            artist = str(audio['artist'])
        length = audio.info.length
        if '/' in artist:
            artists = artist.split('/')
            artist = artists
        else:
            artist = [artist]
        return [title, artist, length]
    except IndexError:
        return None
    except KeyError:
        return None


def wav_duration(_path):
    with contextlib.closing(wave.open(_path, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration
