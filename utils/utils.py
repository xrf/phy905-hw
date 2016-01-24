#@snip/PersistentTemporaryFile[
#@requires: rename
class PersistentTemporaryFile(object):
    '''A context manager for a temporary file that is deleted only if the body
    of the `with` statement fails with some exception.'''

    def __init__(self, filename, mode, suffix=None, prefix=None):
        import os
        self._args = {
            "mode": mode,
            "suffix": ".tmpsave~" if suffix is None else suffix,
            "prefix": "." + os.path.basename(filename)
                      if prefix is None else prefix,
            "dir": os.path.dirname(filename),
            "delete": False,
        }

    def __enter__(self):
        import tempfile
        stream = tempfile.NamedTemporaryFile(**self._args)
        self._tmpfn = stream.name
        return stream

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None and exc_value is None and traceback is None:
            return
        import os
        try:
            os.remove(self._tmpfn)
        except OSError:
            pass
#@]

#@snip/rename[
def rename(src, dest):
    '''Rename a file (allows overwrites on Windows).'''
    import os
    if os.name == "nt":
        import ctypes, ctypes.wintypes
        MoveFileExW = ctypes.windll.kernel32.MoveFileExW
        MoveFileExW.restype = ctypes.wintypes.BOOL
        MOVEFILE_REPLACE_EXISTING = ctypes.wintypes.DWORD(0x1)
        success = MoveFileExW(ctypes.wintypes.LPCWSTR(src),
                              ctypes.wintypes.LPCWSTR(dest),
                              MOVEFILE_REPLACE_EXISTING)
        if not success:
            raise ctypes.WinError()
    else:
        os.rename(src, dest)
#@]

#@snip/read_file[
def read_file(filename, binary=False):
    '''Read the contents of a file.'''
    mode = "r" + ("b" if binary else "t")
    with open(filename, mode) as file:
        contents = file.read()
    return contents
#@]

#@snip/writefile[
#@requires: PersistentTemporaryFile
def write_file(filename, contents, binary=False, safe=True):
    '''Write the contents to a file.  If `safe` is true, it is performed by
    first writing into a temporary file and then replacing the original file
    with the temporary file.  This ensures that the file will not end up in a
    half-written state.  Note that there is a small possibility that the
    temporary file might remain if the program crashes while writing.'''
    mode = "w" + ("b" if binary else "t")
    openfile = PersistentTemporaryFile if safe else open
    with openfile(filename, mode) as stream:
        stream.write(contents)
        rename(stream.name, filename)
#@]
