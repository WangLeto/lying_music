import os
from .read_configure import config_reader
from .read_meta import valid_list, read_meta, wav_duration


class SongsList:
    def __init__(self):
        self.songs = []
        self.refresh()

    def refresh(self):
        self.songs.clear()
        self.__get_list()

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
                    self.__collect_info(os.path.join(r, f), f)

    def __collect_info(self, full_path, file_name):
        ex_name = os.path.splitext(file_name)[-1]
        if ex_name in valid_list:
            # todo too slow
            info = read_meta(full_path)
            if not info:
                return
            if config_reader.duration_valid(info[2]):
                self.songs.append({'title': info[0], 'singers': info[1], 'duration': info[2], 'path': full_path})
        elif ex_name == '.wav':
            duration = wav_duration(full_path)
            if config_reader.duration_valid(duration):
                self.songs.append({'duration': duration, 'path': full_path})
