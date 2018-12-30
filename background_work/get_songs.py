import os
import time
from .read_configure import config_reader
from .read_meta import valid_list, read_meta, wav_duration


class SongsScanner:
    def __init__(self, _global):
        self.songs = []
        self.Global = _global
        self.Global.finished = False

    def refresh(self):
        print('SongsScanner: refresh start scan')
        self.songs.clear()
        self.__get_list()
        time.sleep(7)
        self.Global.finished = True
        print('SongsScanner: refresh finish scan')

    def __get_list(self):
        folders = config_reader.source_folder()
        visited = []
        for folder in folders:
            if folder in visited:
                continue
            visited.append(folder)
            for r, ds, fs in os.walk(folder):
                for d in ds:
                    visited.append(os.path.join(r, d))
                for f in fs:
                    self.__collect_info(f, os.path.join(r, f))

    def __collect_info(self, file_name, full_path):
        entries = []
        ex_name = os.path.splitext(file_name)[-1]
        if ex_name in valid_list:
            info = read_meta(full_path)
            if not info:
                return
            if config_reader.duration_valid(info[2]):
                entries.append({'title': info[0], 'singers': info[1], 'duration': info[2], 'path': full_path})
        elif ex_name == '.wav':
            duration = wav_duration(full_path)
            if config_reader.duration_valid(duration):
                entries.append({'duration': duration, 'path': full_path})
        self.songs += entries
