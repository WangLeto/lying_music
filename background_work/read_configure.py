import yaml
from background_work.user_music_folder import get_music_folders


class _ConfigureReader:
    def __init__(self):
        f = open('CONFIGURE.yml', encoding='utf-8')
        self.content = yaml.load(f)
        self._get_valid_duration()
        f.close()

    def source_folder(self):
        try:
            folder = self.content['music folder']
        except KeyError:
            folder = []
        try:
            use_default_music_folder = self.content['use Windows default music folder']
        except KeyError:
            use_default_music_folder = True
        if use_default_music_folder:
            folder += get_music_folders()
        return folder

    def default_sound_device(self):
        try:
            device = self.content['default device']
        except KeyError:
            return ''
        return device

    def _get_valid_duration(self):
        try:
            _dict = self.content['valid time length']
            self.__valid_duration = (60 * _dict['min'], 60 * _dict['max'])
        except KeyError:
            self.__valid_duration = (60, 15 * 60)

    def duration_valid(self, duration):
        _range = self.__valid_duration
        return _range[0] <= duration <= _range[1]

    def show_player(self):
        try:
            show = self.content['show player']
        except KeyError:
            return False
        return show


config_reader = _ConfigureReader()
