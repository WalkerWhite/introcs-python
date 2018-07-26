"""
Simple wrapper of the urllib.request library

With the elimination of urllib2 AND the move to Unicode, Python 3 has made the first
assignment a lot harder.  These functions are intended to simplify things once again.

:author:  Walker M. White (wmw2)
:version: July 13, 2018
"""


def urlread(url):
    """
    Opens the web page at ``url`` and returns its contents.
    
    If there is no web page at url a ``URLError``. If the url is malformed, it raises a
    ``ValueError`` instead.
    
    :param url: The web page url
    :type url:  ``str``
    
    :return: The contents of the web page at ``url`` if it exists.
    :rtype:  ``str``
    """
    import urllib.request
    connect = urllib.request.urlopen(url)
    header  = connect.info()
    payload = connect.read()
    try:
        return payload.decode('utf-8') # Yeah, no way that was going in A1
    except:
        # We need to find out what the encoding is
        encoding = ''
        for item in header.raw_items():
            if item[0] == 'Content-Type':
                encoding = item[1]
                position = encoding.find('charset=')
                encoding = encoding[position+8:]
    
    if encoding in ['ISO-8859-1','ansi']:
        return payload.decode('latin1')
    elif encoding == 'ascii':
        return payload.decode('ascii')
    else:
        return data.decode('unicode_escape')


def urlinfo(url):
    """
    Returns the headers for the web page at ``url``.
    
    The headers are returned as a dictionary.
    
    If there is no web page at url a ``URLError``. If the url is malformed, it raises a
    ``ValueError`` instead.
    
    :param url: The web page url
    :type url:  ``str``
    
    :return: The headers for the web page at ``url`` if it exists.
    :rtype:  ``dict``
    """
    import urllib.request
    connect = urllib.request.urlopen(url)
    header  = connect.info()
    result = {}
    for item in header.raw_items():
        result[item[0]] = item[1]
    return result

