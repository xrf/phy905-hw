#@snip/TemporarySaveFile[
#@requires: rename try_remove wrapped_open
class TemporarySaveFile(object):
    '''A context manager for a saving files atomically.  The context manager
    creates a temporary file to which data may be written.  If the body of the
    `with` statement succeeds, the temporary file is renamed to the target
    filename, overwriting any existing file.  Otherwise, the temporary file is
    deleted.'''

    def __init__(self, filename, mode="w", suffix=None, prefix=None, **kwargs):
        import os
        self._fn = filename
        kwargs = dict(kwargs)
        kwargs.update({
            "mode": mode,
            "suffix": ".tmpsave~" if suffix is None else suffix,
            "prefix": (".#" + os.path.basename(filename)).rstrip(".") + "."
                      if prefix is None else prefix,
            "dir": os.path.dirname(filename),
            "delete": False,
        })
        self._kwargs = kwargs

    def __enter__(self):
        import shutil, tempfile
        if hasattr(self, "_stream"):
            raise ValueError("attempted to __enter__ twice")
        stream = wrapped_open(tempfile.NamedTemporaryFile, **self._kwargs)
        try:
            shutil.copymode(self._fn, stream.name)
        except BaseException as e:
            import errno
            if not (isinstance(e, OSError) and e.errno == errno.ENOENT):
                try:
                    stream.close()
                finally:
                    try_remove(stream.name)
                raise
        self._stream = stream
        return stream

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self._stream.close()
            if exc_type is None and exc_value is None and traceback is None:
                rename(self._stream.name, self._fn)
            else:
                try_remove(self._stream.name)
        except:
            try_remove(self._stream.name)
            raise
        finally:
            del self._stream
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

#@snip/try_remove[
def try_remove(path):
    import os
    try:
        os.remove(path)
    except OSError:
        return False
    return True
#@]

#@snip/wrapped_open[
def wrapped_open(open, mode="r", encoding=None,
                 errors=None, newline=None, **kwargs):
    '''Enhance an `open`-like function to accept some additional arguments for
    controlling the text processing.  This is mainly done for compatibility
    with Python 2, where these additional arguments are often not accepted.'''
    if "b" in mode:
        if encoding is not None:
            raise Exception("'encoding' argument not supported in binary mode")
        if errors is not None:
            raise Exception("'errors' argument not supported in binary mode")
        if newline is not None:
            raise Exception("'newline' argument not supported in binary mode")
        return open(mode=mode, **kwargs)
    else:
        import io
        mode = mode.replace("t", "") + "b"
        stream = open(mode=mode, **kwargs)
        try:
            return io.TextIOWrapper(stream, encoding=encoding,
                                    errors=errors, newline=newline)
        except:
            stream.close()
            raise
#@]

#@snip/safe_open[
#@requires: TemporarySaveFile
def safe_open(filename, mode="rt", encoding=None,
              errors=None, newline=None, safe=True):
    truncated_write = "w" in mode and "+" not in mode
    if safe and truncated_write and not isinstance(filename, int):
        open_file = TemporarySaveFile
    else:
        from io import open as open_file
    return open_file(filename, mode, encoding=encoding,
                     errors=errors, newline=newline)
#@]

#@snip/load_file[
def load_file(filename, binary=False, encoding=None,
              errors=None, newline=None):
    '''Read the contents of a file.'''
    from io import open
    mode = "r" + ("b" if binary else "")
    with open(filename, mode, encoding=encoding,
              errors=errors, newline=newline) as stream:
        return stream.read()
#@]

#@snip/save_file[
#@requires: safe_open
def save_file(filename, contents, binary=False, encoding=None,
              errors=None, newline=None, safe=True):
    '''Write the contents to a file.  If `safe` is true, it is performed by
    first writing into a temporary file and then replacing the original file
    with the temporary file.  This ensures that the file will not end up in a
    half-written state.  Note that there is a small possibility that the
    temporary file might remain if the program crashes while writing.'''
    mode = "w" + ("b" if binary else "")
    with safe_open(filename, mode, encoding=encoding,
                   errors=errors, newline=newline, safe=safe) as stream:
        stream.write(contents)
#@]

#@snip/save_json_file[
#@requires: safe_open
def save_json_file(filename, contents, encoding=None,
                   errors=None, newline=None, safe=True, json_args={}):
    import json
    with safe_open(filename, "wt", encoding=encoding,
                   errors=errors, newline=newline, safe=safe) as stream:
        json.dump(contents, stream, **dict(json_args))
#@]

#@snip/load_json_file[
def load_json_file(filename, encoding=None, errors=None, newline=None):
    import json
    from io import open
    with open(filename, "rt", encoding=encoding,
              errors=errors, newline=newline) as stream:
        return json.load(stream)
#@]

JSON_ARGS = {
    "indent": 4,
    "separators": (",", ": "),
    "sort_keys": True,
}

def transpose(table):
    return list(zip(*table))

def records_to_dataframe(records):
    import itertools
    records = tuple(records)
    keys = set(itertools.chain(*(record.keys() for record in records)))
    dataframe = dict((key, []) for key in keys)
    for record in records:
        for key in keys:
            dataframe[key].append(record.get(key, None))
    return dataframe

def dataframe_to_records(dataframe):
    dataframe = dict(dataframe)
    if not dataframe:
        return []
    records = []
    keys = tuple(dataframe.keys())
    for i in range(len(dataframe[keys[0]])):
        records.append(dict((key, dataframe[key][i]) for key in keys))
    return records

def group_records_by(records, keys):
    groups = {}
    for record in records:
        group_key = tuple(record[k] for k in keys)
        if group_key not in groups:
            groups[group_key] = []
        groups[group_key].append(record)
    return groups

def tablerows_to_tablecols(table):
    headers = table[0]
    rows = table[1:]
    cols = transpose(rows)
    return dict(zip(headers, cols))

def parse_keyvalue_entry(line, sep):
    key, value = line.split(sep, 1)
    return key.strip(), value.strip()

def parse_keyvalues(string, sep):
    lines = string.split("\n")
    return dict(parse_keyvalue_entry(line, sep) for line in lines if line)

def run_and_get_keyvalues(args):
    import subprocess
    out = subprocess.check_output(args, universal_newlines=True)
    return parse_keyvalues(out, sep="=")

def substitute_template(filename, params):
    import string
    return string.Template(load_file(filename)).substitute(params)

def main_template(html):
    import re
    title = re.match("<h1>(.*)</h1>\n", html).group(1)
    return substitute_template("../utils/template.html", {
        "title": title,
        "body": html,
    })

def table_to_html(rows):
    s = []
    for row in rows:
        s.append("<tr>")
        for cell in row:
            s.extend(["<td>", str(cell), "</td>"])
        s.append("</tr>")
    return "".join(s)

def parse_logging_level(level):
    if level is None:
        return
    level = str(level).upper()
    try:
        return int(level)
    except ValueError:
        pass
    import logging
    lvl = getattr(logging, level, None)
    if isinstance(lvl, int):
        return lvl
    logging.warn("Invalid logging level: " + level)

def init_logging(level=None, default_level=None):
    import logging, os
    config = {
        "format": "[%(levelname)s] %(message)s",
    }
    level = parse_logging_level(level or os.environ.get("LOGLEVEL", None))
    if level is not None:
        config["level"] = level
    elif default_level is not None:
        config["level"] = default_level
    logging.basicConfig(**config)

def register_command(commands):
    def inner(func):
        commands[func.__name__] = func
    return inner

def run_command(commands):
    import sys
    try:
        command = sys.argv[1]
    except IndexError:
        command = ""
    func = commands.get(command, None)
    if not func:
        sys.stderr.write(
            "Unrecognized command: {0}\n"
            "Valid commands are:\n{1}"
            .format(command, "".join("  {0}\n".format(c)
                                     for c in commands))
        )
        exit(2)
    func(*sys.argv[2:])

def merge_means(n1, mean1, n2, mean2):
    n = n1 + n2
    return n, (n1 * mean1 + n2 * mean2) / n

def merge_stdevs(n1, mean1, stdev1, n2, mean2, stdev2):
    n, mean = merge_means(n1, mean1, n2, mean2)
    return n, mean, np.sqrt((
        (n1 - 1) * stdev1 ** 2 + n1 * mean1 ** 2 +
        (n2 - 1) * stdev2 ** 2 + n2 * mean2 ** 2 -
        n * mean ** 2
    ) / (n - 1))
