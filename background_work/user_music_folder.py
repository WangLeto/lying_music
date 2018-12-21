# https://gist.github.com/mkropat/7550097
import os

if os.name == 'nt':
    import ctypes
    from ctypes import windll, wintypes
    from uuid import UUID


    class _GUID(ctypes.Structure):
        _fields_ = [
            ("Data1", wintypes.DWORD),
            ("Data2", wintypes.WORD),
            ("Data3", wintypes.WORD),
            ("Data4", wintypes.BYTE * 8)
        ]

        def __init__(self, uuidstr):
            uuid = UUID(uuidstr)
            ctypes.Structure.__init__(self)
            self.Data1, self.Data2, self.Data3, self.Data4[0], self.Data4[1], rest = uuid.fields
            for i in range(2, 8):
                self.Data4[i] = rest >> (8 - i - 1) * 8 & 0xff


    SHGetKnownFolderPath = windll.shell32.SHGetKnownFolderPath
    SHGetKnownFolderPath.argtypes = [
        ctypes.POINTER(_GUID), wintypes.DWORD,
        wintypes.HANDLE, ctypes.POINTER(ctypes.c_wchar_p)
    ]


    def _get_known_folder_path(uuidstr):
        pathptr = ctypes.c_wchar_p()
        guid = _GUID(uuidstr)
        if SHGetKnownFolderPath(ctypes.byref(guid), 0, 0, ctypes.byref(pathptr)):
            raise ctypes.WinError()
        return pathptr.value


    FOLDERID_Music = '{4BD8D571-6D19-48D3-BE97-422220080E43}'
    FOLDERID_MusicLibrary = '{2112AB0A-C86A-4FFE-A368-0DE96E47012E}'


    def get_music_folders():
        music_folder = _get_known_folder_path(FOLDERID_Music)
        music_library_folder = _get_known_folder_path(FOLDERID_MusicLibrary)
        return [music_folder, music_library_folder]
else:
    def get_music_folders():
        home = os.path.expanduser("~")
        return [os.path.join(home, "Music")]
