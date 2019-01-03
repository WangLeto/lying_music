import subprocess
import ctypes
import os
from .read_configure import config_reader


class Player:
    def __init__(self):
        self.rc = None
        self.args = ['-autoexit']
        show_player = config_reader.show_player()
        if not show_player:
            self.args.append('-nodisp')

    def play(self, path):
        self.rc = subprocess.call(['ffplay', path, *self.args])

    def stop(self):
        pass
        # todo


class SoundDevice:
    def __init__(self):
        _file = 'SoundDevice.dll'
        _path = os.path.join(*(os.path.split(__file__)[:-1] + (_file,)))
        self.lib = ctypes.cdll.LoadLibrary(_path)

    def set_device(self, _id):
        self.lib.SetDefaultSoundDevice(_id)

    def set_default_device(self):
        devices = self.get_devices()
        default_device = config_reader.default_sound_device()
        des_id = 0
        if default_device:
            for index, device in enumerate(devices):
                if default_device.lower() in device.lower() or device.lower() in default_device.lower():
                    des_id = index
                    break
        self.set_device(des_id)

    def get_devices(self):
        func = self.lib.StrSoundDevices
        func.restype = ctypes.c_wchar_p
        devices_str = func()
        return self.__parse_devices_str(devices_str)

    @staticmethod
    def __parse_devices_str(devices_str):
        _list = devices_str.split('\1')
        devices = []
        for item in _list:
            if len(item) != 0:
                devices.append(item)
        return devices
