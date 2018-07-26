"""
Functions for popular string operations.

The purpose of this module is to allow students to work with strings without having to
understand method calls.  We do not provide all string methods as functions -- just the
most popular ones.

The functions that would normally return lists return tuples.  That is because, by the
time students understand lists, they can understand method calls.  However, tuples (since
they are immutable) can be introduced earlier.

:author:  Walker M. White (wmw2)
:version: July 20, 2018
"""


#mark Test Functions
def isalnum(text):
    """
    Checks if all characters in ``text`` are alphanumeric and there is at least one character
    
    A character c is alphanumeric if one of the following returns True: :func:`isalpha`, 
    :func:`isdecimal`,:func:`isdigit`, or, :func:`isnumeric`.
    
    :param text: The string to check
    :type text:  ``str``
    
    :return: True if all characters in ``text`` are alphanumeric and there is at least one character, False otherwise.
    :rtype:  ``bool``
    """
    assert isinstance(text,str), '%s is not a string' % text
    return text.isalnum()


def isalpha(text):
    """
    Checks if all characters in ``text`` are alphabetic and there is at least one character. 
    
    Alphabetic characters are those characters defined in the Unicode character database 
    as a "Letter". Note that this is different from the "Alphabetic" property defined in 
    the Unicode Standard.
    
    :param text: The string to check
    :type text:  ``str``
    
    :return: True if all characters in ``text`` are alphabetic and there is at least one character, False otherwise.
    :rtype:  ``bool``
    """
    assert isinstance(text,str), '%s is not a string' % text
    return text.isalpha()


def isdecimal(text):
    """
    Check if all characters in ``text`` are decimal characters and there is at least one character. 
    
    Decimal characters are those that can be used to form integer numbers in base 10.
    For example, '10' has all decimals, but '1.0' does not (since the period is not a 
    decimal). Formally a decimal character is in the Unicode General Category "Nd".
    
    :param text: The string to check
    :type text:  ``str``
    
    :return: True if all characters in ``text`` are decimal characters and there is at least one character, False otherwise.
    :rtype:  ``bool``
    """
    assert isinstance(text,str), '%s is not a string' % text
    return text.isdecimal()


def isdigit(text):
    """
    Checks if all characters in ``text`` are digits and there is at least one character. 
    
    Digits include decimal characters and digits that need special handling, such as the 
    compatibility superscript digits. This covers digits which cannot be used to form
    numbers in base 10, like the Kharosthi numbers.  It is very rare that this function
    is needed instead of :func:`isdecimal`
    
    :param text: The string to check
    :type text:  ``str``
    
    :return: True if all characters in ``text`` are digits and there is at least one character, False otherwise.
    :rtype:  ``bool``
    """
    assert isinstance(text,str), '%s is not a string' % text
    return text.isdigit()


def islower(text):
    """
    Checks if  all cased characters in ``text`` are lowercase and there is at least one cased character.
    
    Cased characters are defined by the Unicode standard.  All alphabetic characters in the
    ASCII character set are cased.
    
    :param text: The string to check
    :type text:  ``str``
    
    :return: True if all cased characters in ``text`` are lowercase and there is at least one cased character, False otherwise.
    :rtype:  ``bool``
    """
    assert isinstance(text,str), '%s is not a string' % text
    return text.islower()


def isnumeric(text):
    """
    Checks if all characters in ``text`` are numeric characters, and there is at least one character. 
    
    Numeric characters include digit characters, and all characters that have the Unicode 
    numeric value property. These includes all digit characters as well as vulgar fractions
    and Roman numeral (characters). 
    
    :param text: The string to check
    :type text:  ``str``
    
    :return: True if all characters in ``text`` are numeric characters, and there is at least one character, False otherwise.
    :rtype:  ``bool``
    """
    assert isinstance(text,str), '%s is not a string' % text
    return text.isnumeric()


def isprintable(text):
    """
    Checks if all characters in ``text`` are printable or the string is empty. 
    
    Nonprintable characters are those characters defined in the Unicode character database 
    as "Other" or "Separator", excepting the ASCII space (0x20) which is considered printable. 
    Note that printable characters in this context are those which should not be escaped 
    when repr() is invoked on a string. It has no bearing on the handling of strings
    written to sys.stdout or sys.stderr.
    
    :param text: The string to check
    :type text:  ``str``
    
    :return: True if all characters in ``text`` are printable or the string is empty, False otherwise.
    :rtype:  ``bool``
    """
    assert isinstance(text,str), '%s is not a string' % text
    return text.isprintable()


def isspace(text):
    """
    Checks if there are only whitespace characters in ``text`` and there is at least one character. 
    
    Whitespace characters are those characters defined in the Unicode character database 
    as "Other" or "Separator".
    
    :param text: The string to check
    :type text:  ``str``
    
    :return: True if there are only whitespace characters in ``text`` and there is at least one character, False otherwise. 
    :rtype:  ``bool``
    """
    assert isinstance(text,str), '%s is not a string' % text
    return text.isspace()


def isupper(text):
    """
    Checks if all cased characters in ``text`` are uppercase and there is at least one cased character.
    
    Cased characters are defined by the Unicode standard.  All alphabetic characters in the
    ASCII character set are cased.
    
    :param text: The string to check
    :type text:  ``str``
    
    :return: True if all cased characters in ``text`` are uppercase and there is at least one cased character, False otherwise.
    :rtype:  ``bool``
    """
    assert isinstance(text,str), '%s is not a string' % text
    return text.isupper()


pass
#mark -
#mark Conversion Functions

def capitalize(text):
    """
    Creates a copy of ``text`` with only its first character capitalized.
    
    For 8-bit strings, this function is locale-dependent.
    
    :param text: The string to capitalize
    :type text:  ``str``
    
    :return: A copy of ``text`` with only its first character capitalized.
    :rtype: ``str``
    """
    assert isinstance(text,str), '%s is not a string' % text
    return text.capitalize()


def swapcase(text):
    """
    Creates a copy of ``text`` with uppercase characters converted to lowercase and vice versa. 
    
    Note that it is not necessarily true that ``swapcase(swapcase(s)) == s``.  That is
    because of how the Unicode Standard defines cases.
    
    :param text: The string to convert
    :type text:  ``str``
    
    :return: A copy of ``text`` with uppercase characters converted to lowercase and vice versa.
    :rtype: ``str``
    """
    assert isinstance(text,str), '%s is not a string' % text
    return text.swapcase()


def lower(text):
    """
    Creates a copy of ``text`` with all the cased characters converted to lowercase.
    
    The lowercasing algorithm used is described in section 3.13 of the Unicode Standard.
    
    :param text: The string to convert
    :type text:  ``str``
    
    :return: A copy of ``text`` with all the cased characters converted to lowercase.
    :rtype: ``str``
    """
    assert isinstance(text,str), '%s is not a string' % text
    return text.lower()


def upper(text):
    """
    Creates a copy of ``text`` with all the cased characters converted to uppercase. 
    
    Note that ``isupper(upper(s))`` might be False if ``s`` contains uncased characters 
    or if the Unicode category of the resulting character(s) is not "Lu" (Letter, uppercase).
    
    The uppercasing algorithm used is described in section 3.13 of the Unicode Standard.
    
    :param text: The string to convert
    :type text:  ``str``
    
    :return: A copy of ``text`` with all the cased characters converted to uppercase.
    :rtype:  ``str``
    """
    assert isinstance(text,str), '%s is not a string' % text
    return text.upper()


def center(text, width, fillchar= ' '):
    """
    Creates a copy of ``text`` centered in a string of length ``width``.
    
    Padding is done using the specified ``fillchar`` (default is an ASCII space). The original 
    string is returned if ``width`` is less than or equal to len(s).
    
    :param text: The string to center
    :type text:  ``str``
    
    :param width: The width of the stirng to produce
    :type width:  ``int``
    
    :param fillchar: The padding to expand the character to width
    :type fillchar:  ``str``
    
    :return: A copy of ``text`` centered in a string of length ``width``.
    :rtype: ``str``
    """
    assert isinstance(text,str), '%s is not a string' % text
    return text.center(width,fillchar)


def ljust(text, width, fillchar=' '):
    """
    Creates a copy of ``text`` left justified in a string of length ``width``. 
    
    Padding is done using the specified ``fillchar`` (default is an ASCII space). The original 
    string is returned if ``width`` is less than or equal to len(s).
    
    :param text: The string to justify
    :type text:  ``str``
    
    :return: A copy of ``text`` left justified in a string of length ``width``.
    :rtype:  ``str``
    """
    assert isinstance(text,str), '%s is not a string' % text
    return text.ljust(width,fillchar)


def rjust(text, width, fillchar=' '):
    """
    Creates a copy of ``text`` right justified in a string of length ``width``. 
    
    Padding is done using the specified ``fillchar`` (default is an ASCII space). The original 
    string is returned if ``width`` is less than or equal to len(s).
    
    :param text: The string to justify
    :type text:  ``str``
    
    :return: A copy of ``text`` right justified in a string of length ``width``.
    :rtype:  ``str``
    """
    assert isinstance(text,str), '%s is not a string' % text
    return text.rjust(width,fillchar)


def strip(text, chars=None):
    """
    Creates a copy of ``text`` with the leading and trailing characters removed. 
    
    The ``chars`` argument is a string specifying the set of characters to be removed. 
    If omitted or None, the ``chars`` argument defaults to removing whitespace. The ``chars`` 
    argument is not a prefix or suffix; rather, all combinations of its values are stripped::
        
        >>>
        >>> strip('   spacious   ')
        'spacious'
        >>> strip('www.example.com','cmowz.')
        'example'
    
    The outermost leading and trailing ``chars`` argument values are stripped from the string.
    Characters are removed from the leading end until reaching a string character that 
    is not contained in the set of characters in chars. A similar action takes place on 
    the trailing end. For example::
        
        >>>
        >>> comment_string = '#....... Section 3.2.1 Issue #32 .......'
        >>> strip(comment_string,'.#! ')
        'Section 3.2.1 Issue #32'
    
    :param text: The string to copy
    :type text:  ``str``
    
    :param chars: The characters to remove from the ends
    :type chars:  ``str``
    
    :return: A copy of ``text`` with the leading and trailing characters removed.
    :rtype:  ``str``
    """
    assert isinstance(text,str), '%s is not a string' % text
    return text.strip(chars)


def lstrip(text, chars=None):
    """
    Creates a copy of ``text`` with leading characters removed. 
    
    The ``chars`` argument is a string specifying the set of characters to be removed. If 
    omitted or None, the ``chars`` argument defaults to removing whitespace. The ``chars`` 
    argument is not a prefix; rather, all combinations of its values are stripped::
        
        >>>
        >>> lstrip('   spacious   ')
        'spacious   '
        >>> lstrip('www.example.com'.lstrip,'cmowz.')
        'example.com'
    
    :param text: The string to copy
    :type text:  ``str``
    
    :param chars: The leading characters to remove
    :type chars:  ``str``
    
    :return: A copy of ``text`` with the leading characters removed.
    :rtype:  ``str``
    """
    assert isinstance(text,str), '%s is not a string' % text
    return text.lstrip(chars)


def rstrip(text, chars=None):
    """
    Creates a copy of ``text`` with trailing characters removed. 
    
    The ``chars`` argument is a string specifying the set of characters to be removed. If 
    omitted or None, the ``chars`` argument defaults to removing whitespace. The ``chars`` 
    argument is not a suffix; rather, all combinations of its values are stripped::
        
        >>>
        >>> rstrip('   spacious   ')
        '   spacious'
        >>> rstrip('mississippi','ipz')
        'mississ'
    
    :param text: The string to copy
    :type text:  ``str``
    
    :param chars: The trailing characters to remove
    :type chars:  ``str``
    
    :return: A copy of ``text`` with the trailing characters removed.
    :rtype:  ``str``
    """
    assert isinstance(text,str), '%s is not a string' % text
    return text.rstrip(chars)


pass
#mark -
#mark Search Functions

def count_str(text, sub, start=None, end=None):
    """
    Computes the number of non-overlapping occurrences of substring ``sub`` in ``text[start:end]``.
    
    Optional arguments start and end are interpreted as in slice notation.
    
    :param text: The string to search
    :type text:  ``str``
    
    :param sub: The substring to count
    :type sub:  ``str``
    
    :param start: The start of the search range
    :type start:  ``int``
    
    :param end: The end of the search range
    :type end:  ``int``
    
    :return: The number of non-overlapping occurrences of substring ``sub`` in ``text[start:end]``.
    :rtype:  ``int``
    """
    assert isinstance(text,str), '%s is not a string' % text
    return text.count(sub,start,end)


def endswith_str(text, suffix, start=None, end=None):
    """
    Determines if ``text`` ends with the specified suffix. 
    
    The suffix can also be a tuple of suffixes to look for. With optional parameter ``start``, 
    the test will begin at that position. With optional parameter ``end``, the test will
    stop comparing at that position.
    
    :param text: The string to search
    :type text:  ``str``
    
    :param suffix: The suffix to search for
    :type suffix:  ``str`` or ``tuple`` of ``str``
    
    :param start: The start of the search range
    :type start:  ``int``
    
    :param end: The end of the search range
    :type end:  ``int``
    
    :return: True if ``text`` ends with the specified suffix, otherwise return False. 
    :rtype:  ``int``
    """
    assert isinstance(text,str), '%s is not a string' % text
    return text.endswith(suffix,start,end)


def startswith_str(text, prefix, start=None, end=None):
    """
    Determines if ``text`` starts with the specified prefix. 
    
    The prefix can also be a tuple of prefixes to look for. With optional parameter ``start``, 
    the test will begin at that position. With optional parameter ``end``, the test will
    stop comparing at that position.
    
    :param text: The string to search
    :type text:  ``str``
    
    :param prefix: The prefix to search for
    :type prefix:  ``str`` or ``tuple`` of ``str``
    
    :param start: The start of the search range
    :type start:  ``int``
    
    :param end: The end of the search range
    :type end:  ``int``
    
    :return: True if ``text`` starts with the specified prefix, otherwise return False. 
    :rtype:  ``int``
    """
    assert isinstance(text,str), '%s is not a string' % text
    return text.startswith(prefix,start,end)


def find_str(text, sub, start=None, end=None):
    """
    Finds the lowest index of the substring ``sub`` within ``text`` in the range [``start``, ``end``].
    
    Optional arguments ``start`` and ``end`` are interpreted as in slice notation. However,
    the index returned is relative to the original string ``text`` and not the slice
    ``text[start:end]``.  The function returns -1 if ``sub`` is not found.
    
    **Note:** The ``find_str()`` function should be used only if you need to know the position 
    of ``sub``. To check if ``sub`` is a substring or not, use the in operator::
        
        >>>
        >>> 'Py' in 'Python'
        True
    
    :param text: The string to search
    :type text:  ``str``
    
    :param sub: The substring to search for
    :type sub:  ``str``
    
    :param start: The start of the search range
    :type start:  ``int``
    
    :param end: The end of the search range
    :type end:  ``int``
    
    :return: The lowest index of the substring ``sub`` within ``text`` in the range [``start``, ``end``].
    :rtype:  ``int``
    """
    assert isinstance(text,str), '%s is not a string' % text
    return text.find(sub,start,end)


def index_str(text, sub, start=None, end=None):
    """
    Finds the lowest index of the substring ``sub`` within ``text`` in the range [``start``, ``end``].
    
    Optional arguments ``start`` and ``end`` are interpreted as in slice notation. However,
    the index returned is relative to the original string ``text`` and not the slice
    ``text[start:end]``.
    
    This function is like :func:`find_str`, except that it raises a ``ValueError`` when the
    substring is not found.
    
    :param text: The string to search
    :type text:  ``str``
    
    :param sub: The substring to search for
    :type sub:  ``str``
    
    :param start: The start of the search range
    :type start:  ``int``
    
    :param end: The end of the search range
    :type end:  ``int``
    
    :return: The lowest index of the substring ``sub`` within ``text`` in the range [``start``, ``end``].
    :rtype:  ``int``
    """
    assert isinstance(text,str), '%s is not a string' % text
    return text.index(sub,start,end)


def rfind_str(text, sub, start=None, end=None):
    """
    Finds the highest index of the substring ``sub`` within ``text`` in the range [``start``, ``end``].
    
    Optional arguments ``start`` and ``end`` are interpreted as in slice notation. However,
    the index returned is relative to the original string ``text`` and not the slice
    ``text[start:end]``.  The function returns -1 if ``sub`` is not found.
    
    :param text: The string to search
    :type text:  ``str``
    
    :param sub: The substring to search for
    :type sub:  ``str``
    
    :param start: The start of the search range
    :type start:  ``int``
    
    :param end: The end of the search range
    :type end:  ``int``
    
    :return: The highest index of the substring ``sub`` within ``text`` in the range [``start``, ``end``].
    :rtype:  ``int``
    """
    assert isinstance(text,str), '%s is not a string' % text
    return text.rfind(sub,start,end)


def rindex_str(text, sub, start=None, end=None):
    """
    Finds the highest index of the substring ``sub`` within ``text`` in the range [``start``, ``end``].
    
    Optional arguments ``start`` and ``end`` are interpreted as in slice notation. However,
    the index returned is relative to the original string ``text`` and not the slice
    ``text[start:end]``.
    
    This function is like :func:`rfind_str`, except that it raises a ``ValueError`` when the
    substring is not found.
    
    :param text: The string to search
    :type text:  ``str``
    
    :param sub: The substring to search for
    :type sub:  ``str``
    
    :param start: The start of the search range
    :type start:  ``int``
    
    :param end: The end of the search range
    :type end:  ``int``
    
    :return: The highest index of the substring ``sub`` within ``text`` in the range [``start``, ``end``].
    :rtype:  ``int``
    """
    assert isinstance(text,str), '%s is not a string' % text
    return text.rindex(sub,start,end)


def replace_str(text, old, new, count=-1):
    """
    Creates a copy of ``text`` with all occurrences of substring ``old`` replaced by ``new``. 
    
    If the optional argument ``count`` is given, only the first count occurrences are replaced.
     
    :param text: The string to copy
    :type text:  ``str``
    
    :param old: The old string to replace
    :type old:  ``str``
    
    :param new: The new string to replace with
    :type new:  ``str``
    
    :param count: The number of occurrences to replace
    :type count:  ``int``
    
    :return: A copy of ``text`` with all occurrences of substring ``old`` replaced by ``new``. 
    :rtype:  ``str``
    """
    assert isinstance(text,str), '%s is not a string' % text
    return text.replace(old,new,count)


pass
#mark -
#mark Split and Join Functions
def join(iterable,sep=''):
    """
    Creates a string by concatenating the strings in ``iterable``
    
    A TypeError will be raised if there are any non-string values in iterable, including 
    bytes objects. The optional separator is placed between the elements, but by default
    there is no separator.
    
    :param iterable: The iterable of strings to concatenate
    :type iterable:  ``iterable``
    
    :param sep: The separating string
    :type sep:  ``str``
    
    :return: A string which is the concatenation of the strings in iterable. 
    :rtype:  ``str``
    """
    assert isinstance(sep,str), '%s is not a string' % sep
    return sep.join(iterable)


def split(text, sep=None, maxsplit=-1):
    """
    Creates a tuple of the words in ``text``, using ``sep`` as the delimiter string. 
    
    If ``maxsplit`` is given, at most maxsplit splits are done (thus, the tuple will have at 
    most maxsplit+1 elements). If ``maxsplit`` is not specified or -1, then there is no 
    limit on the number of splits (all possible splits are made).
    
    If ``sep`` is given, consecutive delimiters are not grouped together and are deemed to 
    delimit empty strings (for example, ``split('1,,2',',') returns ('1', '', '2')``). The 
    ``sep`` argument may consist of multiple characters (for example, 
    ``split('1<>2<>3','<>')`` returns ``('1', '2', '3')``). Splitting an empty string with 
    a specified separator returns ``('',)``.
    
    For example::
        
        >>>
        >>> split('1,2,3',',')
        ('1', '2', '3')
        >>> split('1,2,3',',', maxsplit=1)
        ('1', '2,3')
        >>> split('1,2,,3,',',')
        ('1', '2', '', '3', '')
    
    If ``sep`` is not specified or is None, a different splitting algorithm is applied. In
    that case runs of consecutive whitespace are regarded as a single separator, and the 
    result will contain no empty strings at the start or end if the string has leading 
    or trailing whitespace. Consequently, splitting an empty string or a string 
    consisting of just whitespace with a None separator returns [].
    
    For example::
        
        >>>
        >>> split('1 2 3')
        ('1', '2', '3')
        >>> split('1 2 3',maxsplit=1)
        ('1', '2 3')
        >>> split('   1   2   3   ')
        ('1', '2', '3')
    
    :param text: The string to split
    :type text:  ``str``
    
    :param sep: The separator to split at
    :type sep:  ``str``
    
    :param maxsplit: The maximum number of splits to perform
    :type maxsplit:  ``int``
    
    :return: A list of the words in ``text``, using ``sep`` as the delimiter string.
    :rtype:  ``str``
    """
    assert isinstance(text,str), '%s is not a string' % text
    return tuple(text.split(sep,maxsplit))


def rsplit(text, sep=None, maxsplit=-1):
    """
    Creates a tuple of the words in ``text``, using ``sep`` as the delimiter string. 
    
    If ``maxsplit`` is given, at most maxsplit splits are done (thus, the tuple will have at 
    most maxsplit+1 elements). If ``maxsplit`` is not specified or -1, then there is no 
    limit on the number of splits (all possible splits are made).
    
    If ``sep`` is given, consecutive delimiters are not grouped together and are deemed to 
    delimit empty strings (for example, ``rsplit('1,,2',',')`` returns ``('1', '', '2')``). 
    The ``sep`` argument may consist of multiple characters (for example, 
    ``rsplit('1<>2<>3','<>')`` returns ``('1', '2', '3')``). Splitting an empty string 
    with a specified separator returns ``('',)``.
    
    This function only differs from :func:`split` if ``maxsplit`` is given and is less than
    the possible number of splits.  In that case, the splits are favored to the right, 
    and so the remainder is to the left.
    
    :param text: The string to split
    :type text:  ``str``
    
    :param sep: The separator to split at
    :type sep:  ``str``
    
    :param maxsplit: The maximum number of splits to perform
    :type maxsplit:  ``int``
    
    :return: A list of the words in ``text``, using ``sep`` as the delimiter string.
    :rtype:  ``str``
    """
    assert isinstance(text,str), '%s is not a string' % text
    return tuple(text.rsplit(sep,maxsplit))


def partition(text, sep):
    """
    Splits ``text`` at the first occurrence of ``sep``, returning the result as 3-tuple.
    
    If the separator is not found, this function returns a 3-tuple containing the 
    string itself, followed by two empty strings.
    
    :return: a 3-tuple containing the part before the separator, the separator itself, and the part after the separator.
    :rtype:  ``tuple`` of ``str``
    """
    assert isinstance(text,str), '%s is not a string' % text
    return text.partition(sep)


def rpartition(text, sep):
    """
    Splits ``text`` at the last occurrence of ``sep``, returning the result as 3-tuple.
    
    If the separator is not found, this function a 3-tuple containing two empty strings, 
    followed by the string itself.
    
    :return: a 3-tuple containing the part before the separator, the separator itself, and the part after the separator.
    :rtype:  ``tuple`` of ``str``
    """
    assert isinstance(text,str), '%s is not a string' % text
    return text.rpartition(sep)




