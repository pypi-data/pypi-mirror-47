import fcntl
import errno
import time
import random


class FileLock():
    def __init__(self, path: str, _disable_lock: bool=False, exclusive: bool=True):
        self._path = path
        self._file = None
        self._disable_lock = _disable_lock
        self._exclusive = exclusive

    def __enter__(self) -> None:
        if self._disable_lock:
            return
        self._file = open(self._path, 'w+')
        num_tries = 0
        while True:
            try:
                if self._exclusive:
                    fcntl.flock(self._file, fcntl.LOCK_EX | fcntl.LOCK_NB)
                else:
                    fcntl.flock(self._file, fcntl.LOCK_SH | fcntl.LOCK_NB)
                if num_tries > 10:
                    print('Locked file {} after {} tries (exclusive={})...'.format(self._path, num_tries, self._exclusive))
                break
            except IOError as e:
                if e.errno != errno.EAGAIN:
                    raise
                else:
                    num_tries = num_tries + 1
                    time.sleep(random.uniform(0, 0.1))

    def __exit__(self, type, value: object, traceback) -> None:
        if self._disable_lock:
            return
        if self._file is not None:
            fcntl.flock(self._file, fcntl.LOCK_UN)
            self._file.close()
