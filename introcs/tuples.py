"""
Functions for popular tuple operations.

The purpose of this module is to allow students to work with tuples without having to
understand method calls.

:author:  Walker M. White (wmw2)
:version: July 20, 2018
"""

def count_tup(tupl, value, start=None, end=None):
    """
    Counts the number of times ``value`` occurs in ``tupl[start:end]``.
    
    Optional arguments start and end are interpreted as in slice notation.
    
    :param tupl: The tuple to search
    :type tupl:  ``tuple``
    
    :param value: The value to count
    :type value:  ``any``
    
    :param start: The start of the search range
    :type start:  ``int``
    
    :param end: The end of the search range
    :type end:  ``int``
    
    :return: The number of times ``value`` occurs in ``tupl[start:end]``.
    :rtype:  ``int``
    """
    assert type(tupl) == tuple, '%s is not a tuple' % tupl
    return tupl[start:end].count(value)


def find_tup(tupl, value, start=None, end=None):
    """
    Finds the lowest index of ``value`` within ``tupl`` in the range [``start``, ``end``].
    
    Optional arguments ``start`` and ``end`` are interpreted as in slice notation. However,
    the index returned is relative to the tuple and not the slice ``tupl[start:end]``.  
    The function returns -1 if ``value`` is not found.
    
    **Note:** The ``find_tup()`` function should be used only if you need to know the position 
    of ``value``. To check if ``value`` is in the tuple, use the in operator::
        
        >>>
        >>> 1 in (1,2,3)
        True
    
    :param tupl: The tuple to search
    :type tupl:  ``tuple``
    
    :param value: The value to search for
    :type value:  ``any``
    
    :param start: The start of the search range
    :type start:  ``int``
    
    :param end: The end of the search range
    :type end:  ``int``
    
    :return: The lowest index of ``value`` within ``tupl`` in the range [``start``, ``end``].
    :rtype:  ``int``
    """
    assert type(tupl) == tuple, '%s is not a tuple' % tupl
    try:
        return index_tup(tupl,value,start,end)
    except ValueError:
        return -1


def index_tup(tupl, value, start=None, end=None):
    """
    Finds the lowest index of ``value`` within ``tupl`` in the range [``start``, ``end``].
    
    Optional arguments ``start`` and ``end`` are interpreted as in slice notation. However,
    the index returned is relative to the tuple and not the slice ``tupl[start:end]``.  
    
    This function is like :func:`find_tup`, except that it raises a ``ValueError`` when the
    value is not found.
    
    :param tupl: The tuple to search
    :type tupl:  ``tuple``
    
    :param value: The value to search for
    :type value:  ``any``
    
    :param start: The start of the search range
    :type start:  ``int``
    
    :param end: The end of the search range
    :type end:  ``int``
    
    :return: The lowest index of ``value`` within ``tupl`` in the range [``start``, ``end``].
    :rtype:  ``int``
    """
    assert type(tupl) == tuple, '%s is not a tuple' % tupl
    # Quick way to enforce slice notation
    segs = tupl[start:end]
    ends = 0 if not start else (start if start >= 0 else len(tupl)+start)
    
    for pos in range(len(segs)):
        if segs[pos] == value:
            return pos+ends
    
    raise ValueError('%s not found in %s' % (repr(value),repr(tupl)))


def rfind_tup(tupl, value, start=None, end=None):
    """
    Finds the highest index of ``value`` within ``tupl`` in the range [``start``, ``end``].
    
    Optional arguments ``start`` and ``end`` are interpreted as in slice notation. However,
    the index returned is relative to the tuple and not the slice ``tupl[start:end]``.  
    The function returns -1 if ``value`` is not found.
    
    :param tupl: The tuple to search
    :type tupl:  ``tuple``
    
    :param value: The value to search for
    :type value:  ``any``
    
    :param start: The start of the search range
    :type start:  ``int``
    
    :param end: The end of the search range
    :type end:  ``int``
    
    :return: The highest index of ``value`` within ``tupl`` in the range [``start``, ``end``].
    :rtype:  ``int``
    """
    assert type(tupl) == tuple, '%s is not a tuple' % tupl
    try:
        return rindex_tup(tupl,value,start,end)
    except ValueError:
        return -1


def rindex_tup(tupl, value, start=None, end=None):
    """
    Finds the highest index of ``value`` within ``tupl`` in the range [``start``, ``end``].
    
    Optional arguments ``start`` and ``end`` are interpreted as in slice notation. However,
    the index returned is relative to the tuple and not the slice ``tupl[start:end]``.  
    
    This function is like :func:`rfind_tup`, except that it raises a ``ValueError`` when the
    value is not found.
    
    :param tupl: The tuple to search
    :type tupl:  ``tuple``
    
    :param value: The value to search for
    :type value:  ``any``
    
    :param start: The start of the search range
    :type start:  ``int``
    
    :param end: The end of the search range
    :type end:  ``int``
    
    :return: The highest index of ``value`` within ``tupl`` in the range [``start``, ``end``].
    :rtype:  ``int``
    """
    assert type(tupl) == tuple, '%s is not a tuple' % tupl
    # Quick way to enforce slice notation
    segs = tupl[start:end]
    size = len(segs)
    ends = 0 if not start else (start if start >= 0 else len(tupl)+start)
    
    for pos in range(size):
        if segs[-pos-1] == value:
            return size-pos-1+ends
    
    raise ValueError('%s not found in %s' % (repr(value),repr(tupl)))


def replace_tup(tupl, old, new, count=-1):
    """
    Creates a copy of ``tupl`` with all occurrences of value ``old`` replaced by ``new``. 
    
    Objects are replaced by value equality, not id equality (i.e. ``==`` not ``is``).
    If the optional argument ``count`` is given, only the first count occurrences are 
    replaced.
     
    :param tupl: The tuple to copy
    :type tupl:  ``tuple``
    
    :param old: The old value to replace
    :type old:  ``any``
    
    :param new: The new value to replace with
    :type new:  ``any``
    
    :param count: The number of occurrences to replace
    :type count:  ``int``
    
    :return: A copy of ``tupl`` with all occurrences of value ``old`` replaced by ``new``. 
    :rtype:  ``tuple``
    """
    assert type(tupl) == tuple, '%s is not a tuple' % tupl
    result = []
    count = len(tupl) if count == -1 else count
    match = 0
    for item in tupl:
        if item == old and match < count:
            result.append(new)
            match += 1
        else:
            result.append(item)
    return tuple(result)
