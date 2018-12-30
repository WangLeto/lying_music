from background_work.get_songs import SongsScanner
from music_web.hello import app, import_global
from multiprocessing import Manager, Process

if __name__ == '__main__':
    manager = Manager()
    Global = manager.Namespace()
    songs_scanner = SongsScanner(Global)
    process = Process(target=songs_scanner.refresh)
    process.start()

    import_global(Global)
    app.debug = True
    app.run(port=8002, use_reloader=False)
