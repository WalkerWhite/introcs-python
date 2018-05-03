"""
Simple wrapper of the urllib.request library

With the elimination of urllib2 AND the move to Unicode, Python 3 has made the first
assignment a lot harder.  These functions are intended to simplify things once again.

Author: Walker M. White (wmw2)
Date:   July 20, 2017
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
    connection = urllib.request.urlopen(url)
    return connection.read().decode('utf-8') # Yeah, no way that was going in A1


def urlinfo(url):
    """
    Returns the headers for the web page at ``url``.
    
    The headers are returned as a dictionary, hence order is not preserved.
    
    If there is no web page at url a ``URLError``. If the url is malformed, it raises a
    ``ValueError`` instead.
    
    :param url: The web page url
    :type url:  ``str``
    
    :return: The headers for the web page at ``url`` if it exists.
    :rtype:  ``dict``
    """
    import urllib.request
    connection = urllib.request.urlopen(url)
    header = connection.info()
    result = {}
    for item in header.raw_items():
        result[item[0]] = item[1]
    return result


def isredirected(url):
    """
    Attempts to connect to ``url`` and determines if it was redirected.
    
    If there is no web page at url a ``URLError``. If the url is malformed, it raises a
    ``ValueError`` instead.
    
    :param url: The web page url
    :type url:  ``str``
    
    :return: True is the connect to ``url`` requires a redirection.
    :rtype:  ``bool``
    """
    import urllib.request
    connection = urllib.request.urlopen(url)
    return url == connection.geturl()