import os.path,random,re,json
from werkzeug._compat import unichr, text_type,PY2

#_filename_ascii_strip_re = re.compile(r'[^A-Za-z0-9_.-]') #for ascii
_filename_ascii_strip_re = re.compile(ur'[^\u4e00-\u9fa5A-Za-z0-9_.-]')

def secure_filename(filename):
    r"""Pass it a filename and it will return a secure version of it.  This
    filename can then safely be stored on a regular file system and passed
    to :func:`os.path.join`.  The filename returned is an unicode string
    compared to the original version secure_filename() from werkzeug
    On windows systems the function also makes sure that the file is not
    named after one of the special device files.
    >>> secure_filename("My cool movie.mov")
    'My_cool_movie.mov'
    >>> secure_filename("../../../etc/passwd")
    'etc_passwd'
    The function might return an empty filename.  It's your responsibility
    to ensure that the filename is unique and that you generate random
    filename if the function returned an empty one.
    .. versionadded:: 0.5
    :param filename: the filename to secure
    """
    if isinstance(filename, text_type):
        from unicodedata import normalize
        filename = normalize('NFKD', filename) #.encode('ascii', 'ignore')
        if not PY2:
            filename = filename.decode('ascii')
    for sep in os.path.sep, os.path.altsep:
        if sep:
            filename = filename.replace(sep, ' ')
    #filename = str(_filename_ascii_strip_re.sub('', '_'.join(
    #               filename.split()))).strip('._')
    filename = _filename_ascii_strip_re.sub('', '_'.join(filename.split())).strip('._')

    # on nt a couple of special files are present in each folder.  We
    # have to ensure that the target file is not such a filename.  In
    # this case we prepend an underline
    if os.name == 'nt' and filename and \
       filename.split('.')[0].upper() in _windows_device_files:
        filename = '_' + filename

    return filename