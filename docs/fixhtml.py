#!/usr/bin/env python
"""
HTML Fixing Script

I am not a fan of everything that Sphinx does in its autogeneration.  For example,
prepending a method name by the module is a very bad design decision.  This fixes
these issues.

:author:  Walker M. White.
:version: July 26, 2018
"""
import re
import os
import traceback

def fix(filename):
    """
    Do the fixing.
    """
    
    # Read the file.
    f = open(filename,'r')
    string = f.read()
    f.close()
    
    string = fix_args(string)
    string = fix_assert_error(string)
    string = fix_attributes(string)
    string = fix_methods(string)
    
    # Save
    f = open(filename,'w')
    f.write(string)
    f.close()


def fix_args(string):
    """
    Hide default values and use standard [] notation for optionals.
    
    This makes our documentation closer to the Python API
    """
    # Hide default values
    defs = re.compile('<span class="sig-paren">\(</span>(?P<args>[^\)]*)<span class="sig-paren">\)</span>')
    opts = re.compile('<em class="sig-param">(?P<var>[^=<]*)=(?P<val>[^<]*)</em>')
    
    prefix = ''
    remain = string
    
    match = defs.search(remain)
    while match:
        prefix += remain[:match.start(1)]
        prefargs = ''
        remnargs = remain[match.start(1):match.end(1)]
        optional = opts.search(remnargs)
        count = 0
        while optional:
            prefargs += remnargs[:optional.start(0)]+'<strong>[</strong>'
            prefargs += remnargs[optional.start(0):optional.end(1)]
            prefargs += remnargs[optional.end(2):optional.end(0)]
            remnargs = remnargs[optional.end(0):]
            optional = opts.search(remnargs)
            count += 1
        if count:
            prefargs += '<strong>'+']'*count+'</strong>'
        prefix += prefargs+remnargs
        prefix += remain[match.end(1):match.end(0)]
        remain = remain[match.end(0):]
        match = defs.search(remain)
    return prefix+remain


def fix_assert_error(string):
    defs = re.compile('<code class="sig-name descname">assert_error</code><span class="sig-paren">\(</span>(?P<args>[^\)]*)<span class="sig-paren">\)</span>')
    prefix = ''
    remain = string
    match = defs.search(remain)
    while match:
        prefix += remain[:match.start(1)]
        prefix += '<em class="sig-param">func</em>, <em class="sig-param">*args</em>, <em class="sig-param">error=AssertionError</em>, <em class="sig-param">reason=None</em>,<br/>'
        prefix += '<span style="padding-left:11.6em" /><em class="sig-param">message=None</em>'
        prefix += remain[match.end(1):match.end(0)]
        remain = remain[match.end(0):]
        match = defs.search(remain)
    
    return prefix+remain
    


def fix_attributes(string):
    """
    Remove the class prefix for any attribute.
    
    Honestly Sphinx, why do you do this?
    """
    defs = re.compile('<dl class="attribute">(?P<descrip>.*?)</dl>',flags=re.DOTALL)
    name = re.compile('<code class="descclassname">(?P<name>[^<]*)</code>')
    prefix = ''
    remain = string
    
    match = defs.search(remain)
    while match:
        prefix += remain[:match.start(1)]
        prefsub = ''
        remnsub = remain[match.start(1):match.end(1)]
        descrip = name.search(remnsub)
        if descrip:
            prefix += remnsub[:descrip.start()]
            prefix += remnsub[descrip.end():]
            prefix += remain[match.end(1):match.end(0)]
        else:
            prefix += remain[match.start(1):match.end(0)]
        remain = remain[match.end(0):]
        match = defs.search(remain)
    return prefix+remain


def fix_methods(string):
    """
    Remove the class prefix for any method that is NOT a classmethod.
    
    Replaces the prefix with self to better match the documentation.
    
    Honestly Sphinx, why do you do this?
    """
    defs = re.compile('<dl class="method">(?P<descrip>.*?)</dl>',flags=re.DOTALL)
    name = re.compile('<code class="descclassname">(?P<name>[^<]*)</code>')
    prefix = ''
    remain = string
    
    match = defs.search(remain)
    while match:
        prefix += remain[:match.start(1)]
        prefsub = ''
        remnsub = remain[match.start(1):match.end(1)]
        descrip = name.search(remnsub)
        if descrip:
            prefix += remnsub[:descrip.start(1)]
            prefix += 'self.'
            prefix += remnsub[descrip.end(1):]
            prefix += remain[match.end(1):match.end(0)]
        else:
            prefix += remain[match.start(1):match.end(0)]
        remain = remain[match.end(0):]
        match = defs.search(remain)
    return prefix+remain


def isrst(filename):
    """
    Returns true if filename is an rst
    """
    return filename[-4:] == '.rst'


def tohtml(filename):
    """
    Gets the html file for an rst
    """
    return './_build/html/'+filename[:-4]+'.html'


def main():
    """
    Runs the filter
    """
    lst = filter(isrst,os.listdir('.'))
    for x in lst:
        try:
            fix(tohtml(x))
        except:
            traceback.print_exc()
            pass

        
if __name__ == '__main__':
    main()