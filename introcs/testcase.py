"""
Unit test functions for Python

This module provides function-level unit testing tools.  It is a replacement for the 
built-in Python package unittest, which is much less user friendly and requires an 
understanding of OO programming. 

The assert functions in this module are different from standard assert statements.
They stop execution of Python and report the location of the error.

:author:  Walker M. White (wmw2)
:version: June 7, 2019
"""
import math


def isfloat(s):
    """
    Checks whether the string ``s`` represents a float.
    
    :param s: the candidate string to test
    :type s:  ``str``
    
    :return: True if s is the string representation of a number
    :rtype:  ``bool``
    """
    try:
        x = float(s)
        return True
    except:
        return False


def isint(s):
    """
    Checks whether the string ``s`` represents an integer.
    
    :param s: the candidate string to test
    :type s:  ``str``
    
    :return: True if s is the string representation of an integer
    :rtype:  ``bool``
    """
    try:
        x = int(s)
        return True
    except:
        return False


def isbool(s):
    """
    Checks whether the string ``s`` represents a boolean.
    
    The string requires Python capitalization (e.g. 'True', not 'true').
    
    :param s: the candidate string to test
    :type s:  ``str``
    
    :return: True if s is the string representation of a boolean
    :rtype:  ``bool``
    """
    if type(s) in [int,float,bool]:
        return True
    elif (type(s) != str):
        return False
    return s in ['True','False']


def allclose(a, b, rtol=1e-05, atol=1e-08, equal_nan=False):
    """
    Returns True if two sequences are element-wise equal within a tolerance.
    
    The values a and b are expected to be sequences, though they can be nested sequences
    so long as the base elements are numbers (int or float).  For example, ((1,2), (3,4))
    is an acceptable value but ((1,2),('a',3)) is not.  In addition, the inputs are 
    expected to have the same 'shape' (same length overall and for any nested elements).
    
    The tolerance values are positive, and are typically very small numbers. The relative 
    difference (`rtol` * abs(`b`)) and the absolute difference `atol` are added together 
    to compare against the absolute difference between `a` and `b`.
    
    If either sequences contains one or more NaNs, False is returned (unless equal_nan
    is True). Infs are treated as equal if they are in the same place and of the same 
    sign in both sequences.
    
    This is a safe replacement for the numpy version.
    
    Examples::
        
        isclose([1],[1.000001]) is True
        isclose([1,2.01],[1.000001,2]) is False
        isclose([[1,2],[3,4]],[[1,2],[3,4]]) is True
    
    :param a: Input sequence to compare
    :type a:  sequence
    
    :param b: Input sequence to compare
    :type b:  sequence
    
    :param rtol: The relative tolerance parameter (Optional).
    :type rtol:  ``float``
    
    :param atol: The absolute tolerance parameter (Optional).
    :type atol: ``float``
    
    :param equal_nan: Whether to compare NaN’s as equal (Optional).
    :type equal_nan:  ``bool``
    """
    if type(a) in [float,int] and type(b) in [float,int]:
        return abs(a-b) <= atol + rtol * abs(b)
    
    error = None
    messg = None
    try:
        return _close_descent(a,b,rtol,atol,equal_nan)
    except TypeError as e:
        error = TypeError
        bad = b
        if e.args[0] == 1:
            bad = a
        if type(bad) in [bool,str]:
            messg = '%s has the wrong type' % repr(bad)
        else:
            messg = '%s has invalid contents' % repr(bad)
    except ValueError as f:
        error = ValueError
        messg = '%s and %s do not have the same shape' %(repr(a),repr(b))
    
    if error:
        raise error(messg)
    
    raise RuntimeError('An unknown error has occurred')


def isclose(a, b, rtol=1e-05, atol=1e-08, equal_nan=False):
    """
    Returns a boolean or sequence comparing to inputs element-wise within a tolerance.
    
    The values a and b can either be numbers (``int`` or ``float``) or a sequence.  If
    they are numbers, this function returns a boolean.
    
    If they are sequences, they can be nested, but their base elements must be numbers 
    (int or float).  For example, ((1,2), (3,4))is an acceptable value but ((1,2),('a',3)) 
    is not. In addition, the inputs are expected to have the same 'shape' (same length 
    overall and for any nested elements). The value returned will be a sequence of 
    booleans of the same shape as the inputs.
    
    The tolerance values are positive, typically very small numbers.  The relative 
    difference (`rtol` * abs(`b`)) and the absolute difference `atol` are added together 
    to compare against the absolute difference between `a` and `b`.
    
    This is a safe replacement for the numpy version.
    
    Examples::
        
        isclose(1,1.000001) is True
        isclose([1,2.01],[1.000001,2]) is [True,False]
        isclose([[1,2],[5,4]],[[1,2],[3,4]]) is [[True,True],[False,True]]
    
    :param a: Input to compare
    :type a:  number or sequence
    
    :param b: Input sequence to compare
    :type b:  number or sequence
    
    :param rtol: The relative tolerance parameter (Optional).
    :type rtol:  ``float``
    
    :param atol: The absolute tolerance parameter (Optional).
    :type atol:  ``float``
    
    :param equal_nan: Whether to compare NaN’s as equal (Optional).
    :type equal_nan:  ``bool``
    
    :return: a boolean or sequence comparing to inputs element-wise
    :rtype: ``bool`` or sequence 
    """
    if type(a) in [float,int] and type(b) in [float,int]:
        return abs(a-b) <= atol + rtol * abs(b)
    
    error = None
    messg = None
    try:
        return _close_descent(a,b,rtol,atol,equal_nan,False)
    except TypeError as e:
        error = TypeError
        bad = b
        if e.args[0] == 1:
            bad = a
        if type(bad) in [bool,str]:
            messg = '%s has the wrong type' % repr(bad)
        else:
            messg = '%s has invalid contents' % repr(bad)
    except ValueError as f:
        error = ValueError
        messg = '%s and %s do not have the same shape' %(repr(a),repr(b))
    
    if error:
        raise error(messg)
    
    raise RuntimeError('An unknown error has occurred')



def _close_descent(a, b, rtol, atol, equal_nan, flatten=True):
    """
    Returns a boolean or sequence comparing to inputs element-wise within a tolerance.
    
    This is a recursive function intended to implement `allclose` and `isclose`
    Which one it implements depends on the value of `flatten`.  If `flatten` is True,
    it returns a boolean.  Otherwise it returns a value of the same shape as the inputs.
    
    This method uses coded exceptions to abort if the inputs are invalid.
    
    :param a: Input to compare
    :type a:  number or sequence
    
    :param b: Input sequence to compare
    :type b:  number or sequence
    
    :param rtol: The relative tolerance parameter (Optional).
    :type rtol:  ``float```
    
    :param atol: The absolute tolerance parameter (Optional).
    :type atol:  ``float```
    
    :param equal_nan: Whether to compare NaN’s as equal (Optional).
    :type equal_nan:  ``bool```
    
    :param flatten: Whether to flatten the final answer (Optional)
    :type flatten: ``bool``
    
    :return: a boolean or sequence comparing to inputs element-wise
    :rtype: ``bool`` or sequence 
    """
    if type(a) in [float,int]:
        if not type(b) in [float,int]:
            try:
                test = b[0]
            except:
                raise ValueError()   # Shape mismatch
            raise TypeError(2)       # Content mismatch
        elif math.isinf(a) or math.isinf(b):
            return math.isinf(a) and math.isinf(b)
        elif not math.isnan(a) and not math.isnan(b):
            return abs(a-b) <= atol + rtol * abs(b)
        elif equal_nan:
            return math.isnan(a) and math.isnan(b)
        else:
            return False
    elif type(b) in [float,int]:
        try:
            test = a[0]
        except:
            raise ValueError()      # Shape mismatch
        raise TypeError(1)          # Content mismatch
    
    try:
        test = a[0]
    except:
        raise TypeError(1)          # Content mismatch
    try:
        test = b[0]
    except:
        raise TypeError(2)          # Content mismatch
    
    if len(a) != len(b):
        raise ValueError(6)
    
    if flatten:
        result = True
        for pos in range(len(a)):
            result = result and _close_descent(a[pos],b[pos],rtol, atol, equal_nan, flatten)
    else:
        result = []
        for pos in range(len(a)):
            result.append(_close_descent(a[pos],b[pos],rtol, atol, equal_nan, flatten))
    
    return  result


def quit_with_error(msg):
    """
    Quits Python with an error msg
    
    When testing, this is preferable to raising an error in Python. Once you have a lot 
    of helper functions, it becomes a lot of work just to figure out what is going on in 
    the error message. This makes the error clear and concise
    
    :param msg: The error message
    :type msg:  ``str``
    """
    import traceback
    stack = traceback.extract_stack()
    frame = stack[-3]
    print(msg)
    if (frame[3] is None):
        suffix = ''
    else:
        suffix = ": "+frame[3]
    print('Line',repr(frame[1]),'of',frame[0] + suffix)
    print('Quitting with Error')
    raise SystemExit()


def assert_equals(expected,received,message=None):
    """
    Quits if ``expected`` and ``received`` differ.
    
    The meaning of "differ" for this function is !=.  As a result, this assert function 
    is not necessarily reliable when expected and received are of type ``float``.  You 
    should use the function :func:`assert_floats_equal` for that application.
    
    If there is no custom error message, this function will print some minimal debug
    information. The following is an example debug message::
        
        assert_equals: expected 'yes' but instead got 'no'
    
    :param expected: The value you expect the test to have
    
    :param received: The value the test actually had
    
    :param message: A custom error message (OPTIONAL)
    :type message: ``str``
    """
    if (expected != received):
        if message is None:
            message = 'assert_equals: expected %s but instead got %s' % (repr(expected),repr(received))
        quit_with_error(message)


def assert_not_equals(expected,received,message=None):
    """
    Quits if ``expected`` and ``received`` differ.
    
    The meaning of "differ" for this function is !=.  As a result, this assert function 
    is not necessarily reliable when expected and received are of type ``float``.  You 
    should use the function :func:`assert_floats_not_equal` for that application.
    
    If there is no custom error message, this function will print some minimal debug
    information. The following is an example debug message::
        
        assert_not_equals: expected something different from 'n' 
    
    :param expected: The value you expect the test to have
    
    :param received: The value the test actually had
    
    :param message: A custom error message (OPTIONAL)
    :type message: ``str``
    """
    if (expected == received):
        if message is None:
            message = 'assert_not_equals: expected something different from %s' % repr(expected)
        quit_with_error(message)


def assert_true(received,message=None):
    """
    Quits if ``received`` is False.
    
    If there is no custom error message, this function will print some minimal debug
    information. The following is an example debug message::
        
        assert_true: expected True but instead got False
    
    :param received: The value the test actually had
    
    :param message: A custom error message (OPTIONAL)
    :type message: ``str``
    """
    if (not received):
        if message is None:
            message = 'assert_true: %s evaluates to False' % repr(received)
        quit_with_error(message)


def assert_false(received,message=None):
    """
    Quits if ``received`` is True.
    
    If there is no custom error message, this function will print some minimal debug
    information. The following is an example debug message::
        
        assert_false: expected False but instead got True
    
    :param received: The value the test actually had
    
    :param message: A custom error message (OPTIONAL)
    :type message: ``str``
    """
    if (received):
        if message is None:
            message = 'assert_false: %s evaluates to True' % repr(received)
        quit_with_error(message)


def assert_floats_equal(expected, received,message=None):
    """
    Quits if the floats ``expected`` and ``received`` differ.
    
    This function takes two numbers and compares them using functions from the numerical 
    package ``numpy``.  This is a scientific computing package that allows us to test if 
    numbers are "close enough". Hence, unlike :func:`assert_equal`, the meaning of 
    "differ" for  this function is defined by numpy.
    
    If there is no custom error message, this function will print some minimal debug
    information. The following is an example debug message::
        
        assert_floats_equal: expected 0.1 but instead got 0.2
    
    **IMPORTANT**: 
    The arguments expected and received should each numbers (either floats or ints). If 
    either argument is not a number, the function quits with a different error message. 
    For example::
    
        assert_floats_equal: first argument 'alas' is not a number
    
    :param expected: The value you expect the test to have
    :type expected:  ``float``
    
    :param received: The value the test actually had
    :type received:  ``float``
    
    :param message: A custom error message (OPTIONAL)
    :type message: ``str``
    """
    number = [float, int]  # list of number types
    if type(expected) not in number:
        if message is None:
            message = ('assert_floats_equal: first argument %s is not a number' % repr(expected))
    elif type(received) not in number:
        if message is None:
            message = ('assert_floats_equal: second argument %s is not a number' % repr(received))
    elif (not isclose(expected,received)):
        if message is None:
            message = 'assert_floats_equal: expected %s but instead got %s' % (repr(expected),repr(received))
    else:
        message = None
    
    if not message is None:
        quit_with_error(message)


def assert_floats_not_equal(expected, received,message=None):
    """
    Quits if floats ``expected`` and ``received`` are the same.
    
    This function takes two numbers and compares them using functions from the numerical 
    package ``numpy``.  This is a scientific computing package that allows us to test if 
    numbers are "close enough".  Hence, unlike :func:`assert_not_equal`, the meaning of 
    "same" for  this function is defined by numpy.
    
    If there is no custom error message, this function will print some minimal debug
    information. The following is an example debug message::
        
        assert_floats_not_equal: expected something different from 0.1 
    
    **IMPORTANT**: 
    The arguments expected and received should each numbers (either floats or ints). If 
    either argument is not a number, the function quits with a different error message. 
    For example::
        
         assert_floats_not_equal: first argument 'alas' is not a number
    
    :param expected: The value you expect the test to have
    :type expected:  ``float``
    
    :param received: The value the test actually had
    :type received:  ``float``
    
    :param message: A custom error message (OPTIONAL)
    :type message: ``str``
    """
    number = [float, int]  # list of number types
    if type(expected) not in number:
        if message is None:
            message = ('assert_floats_not_equal: first argument %s is not a number' % repr(expected))
    elif type(received) not in number:
        if message is None:
            message = ('assert_floats_not_equal: second argument %s is not a number' % repr(received))
    elif (isclose(expected,received)):
        if message is None:
            message = ('assert_floats_not_equal: expected something different from %s' % repr(expected))
    else:
        message = None
    
    if not message is None:
        quit_with_error(message)


def _check_nested_floats(thelist):
    """
    Returns True if thelist is a (nested) list of floats
    
    INTERNAL HELPER
    
    If thelist recursively contains anything other than a list, tuple, int, or float,
    this function returns false.
    
    :param message: A custom error message (OPTIONAL)
    :type message: ``str``
    """
    result = True
    for item in thelist:
        if type(item) in [list,tuple]:
            result = result and _check_nested_floats(item)
        else:
            result = result and type(item) in [int,float]
    return result


def assert_float_lists_equal(expected, received,message=None):
    """
    Quits if the lists (or tuples) of floats ``expected`` and ``received`` differ
    
    This function takes two numbers and compares them using functions from the numerical 
    package ``numpy``.  This is a scientific computing package that allows us to test if 
    numbers are "close enough".  Hence, unlike :func:`assert_equal`, the meaning of 
    "differ" for  this function is defined by numpy.
    
    This function is similar to :func:`assert_floats_equal`. The difference is that it 
    works on lists of floats.  These lists can be multidimensional.  To illustrate this, 
    the following is an example debug message::
        
        assert_float_lists__equal: expected [[1,2],[3,4]] but instead got [[1,2],[3,5]]
    
    If there is a custom error message, that will be used instead.
    
    **IMPORTANT**: 
    The arguments expected and received should each lists of numbers. Furthemore, they 
    must have EXACTLY the same dimension.  If not this function quits with a different 
    error message.  For example::
       
        assert_float_lists_equal: first argument 'alas' is not a sequence
    
    or also::
        
        assert_float_lists_equal: sequences [1] and [2,3] have different sizes
    
    :param expected: The value you expect the test to have
    :type expected:  ``list`` or ``tuple``
    
    :param received: The value the test actually had
    :type received:  ``list`` or ``tuple``
    
    :param message: A custom error message (OPTIONAL)
    :type message: ``str``
    """
    error = True
    if not type(expected) in [list,tuple]:
        if message is None:
            message = ('assert_float_lists_equal: first argument %s is not a sequence' % repr(expected))
    elif not type(received) in [list,tuple]:
        if message is None:
            message = ('assert_float_lists_equal: second argument %s is not a sequence' % repr(received))
    elif not _check_nested_floats(expected):
        if message is None:
            message = ( 'assert_float_lists_equal: first argument %s has non-numeric values' % repr(expected))
    elif not _check_nested_floats(received):
        if message is None:
            message = ( 'assert_float_lists_equal: second argument %s has non-numeric values' % repr(received))
    elif len(expected) != len(received):
        if message is None:
            message = ( 'assert_float_lists_equal: sequences %s and %s have different sizes' % 
                        (repr(expected),repr(received)))
    else:
        error = False
    
    if error:
        quit_with_error(message)
    
    test = True
    try:
        if not allclose(expected,received):
            error = True
            if message is None:
                message = 'assert_float_lists_equal: expected %s but instead got %s' % (repr(expected),repr(received))
    except Exception as e:
        error = True
        if message is None:
            message = 'assert_float_lists_equal: sequences %s and %s are not comparable' % (repr(expected),repr(received))
    
    if error:
        quit_with_error(message)


def assert_float_lists_not_equal(expected, received,message=None):
    """
    Quits if the lists (or tuples) of floats ``expected`` and ``received`` are the same
    
    This function takes two numbers and compares them using functions from the numerical 
    package ``numpy``.  This is a scientific computing package that allows us to test if 
    numbers are "close enough".  Hence, unlike :func:`assert_not_equal`, the meaning of 
    "same" for  this function is defined by numpy.
    
    This function is similar to :func:`assert_floats_not_equal`. The difference is that it 
    works on lists of floats.  These lists can be multidimensional.  To illustrate this, 
    the following is an example debug message::
        
        assert_float_lists_not_equal: expected something different from [[1,2],[3,4]] 
    
    **IMPORTANT**: 
    The arguments expected and received should each be sequences of numbers. If not this
    function quits with a different error message.  For example::
           
        assert_float_lists_not_equal: first argument 'alas' is not a list
    
    or also::
        
        assert_float_lists_not_equal: first argument (1, 'a') has non-numeric values
    
    It is not a problem if the sequences have different dimensions as long as they are
    numeric. In that case, the function will not quit with an error. 
    
    If there is a custom error message, that will be used instead.
    
    :param expected: The value you expect the test to have
    :type expected:  ``list`` or ``tuple``
    
    :param received: The value the test actually had
    :type received:  ``list`` or ``tuple``
    
    :param message: A custom error message (OPTIONAL)
    :type message: ``str``
    """
    error = True
    if not type(expected) in [list,tuple]:
        if message is None:
            message = ('assert_float_lists_not_equal: first argument %s is not a sequence' % repr(expected))
    elif not type(received) in [list,tuple]:
        if message is None:
            message = ('assert_float_lists_not_equal: second argument %s is not a sequence' % repr(received))
    elif not _check_nested_floats(expected):
        if message is None:
            message = ( 'assert_float_lists_not_equal: first argument %s has non-numeric values' % repr(expected))
    elif not _check_nested_floats(received):
        if message is None:
            message = ( 'assert_float_lists_not_equal: second argument %s has non-numeric values' % repr(received))
    elif len(expected) != len(received):
        return
    else:
        error = False
    
    if error:
        quit_with_error(message)
    
    test = True
    try:
        if allclose(expected,received):
            error = True
            if message is None:
                message = 'assert_float_lists_not_equal: expected something different from %s' % repr(expected)
    except ValueError:
        pass
    except Exception as e:
        error = True
        if message is None:
            message = 'assert_float_lists_not_equal: sequences %s and %s are not comparable' % (repr(expected),repr(received))
    
    if error:
        quit_with_error(message)


def assert_error(func,*args,error=AssertionError,reason=None,message=None):
    """
    Quits if call func(\*args) does not crash with the given error.
    
    This function calls func(\*args) and checks whether it crashes with the given error 
    (AssertionError by default).  If the call does not crash, or crashes with a different 
    error, this function will quit with an error message.
    
    The optional argument reason checks against the ``args`` attribute of the error 
    (i.e. the error reason), provided that it is not None. If reason is a tuple, it 
    will compare the value to args using ==.  Otherwise, if it is any type other than 
    None, it will compare against the first element of ``args``.
    
    The optional argument message is for the error message to print should this 
    function fail (i.e. it is not the error "message" of the error being tested). If 
    there is no custom error message, this function will print some minimal debug
    information. The following is an example debug message::
        
        assert_error: call foo(1) did not crash but instead returned 42
    
    or also::
        
        assert_error: call foo(1) crashed with TypeError, not AssertionError
    
    :param func: The function to test for enforcement
    :type func:  ``callable``
    
    :param args: The function arguments
    :type args:  ``tuple``
    
    :param error: The expected error type (OPTIONAL)
    :type error:  ``class``
    
    :param reason: The expected error reason (OPTIONAL)
    :type reason:  any
    
    :param message: A custom error message (OPTIONAL)
    :type message: ``str``
    """
    failed = True
    if not callable(func):
        if message is None:
            message = ('assert_error: argument %s is not callable' % repr(func))
    else:
        try:
            result = func(*args)
            if message is None:
                body = repr(args) if len(args) != 1 else '(%s)' % repr(args[0])
                message = ('assert_error: call %s%s did not crash but instead returned %s' % (func.__name__, body, repr(result)))
        except BaseException as e:
            if e.__class__ == error:
                failed = False
                if type(reason) == tuple:
                    if reason != e.args:
                        failed = True
                        if message is None:
                            name = e.__class__.__name__
                            message = ('assert_error: %s has reason %s, not %s' % (name, repr(e.args), repr(reason)))
                elif not reason is None: 
                    if len(e.args) == 0 or reason != e.args[0]:
                        failed = True
                        if message is None:
                            name = e.__class__.__name__
                            if len(e.args) == 0:
                                message = ('assert_error: %s has no reason, but expected %s' % (name, repr(reason)))
                            else:
                                payload = e.args[0] if len(e.args) == 1 else e.args
                                message = ('assert_error: %s has reason %s, not %s' % (name, repr(payload), repr(reason)))
            elif message is None:
                name1 = e.__class__.__name__
                name2 = error.__name__
                body = repr(args) if len(args) != 1 else '(%s)' % repr(args[0])
                message = ('assert_error: call %s%s crashed with %s, not %s' % (func.__name__, body, name1, name2))
    
    if failed:
        quit_with_error(message)

