"""
Tools to simplify the loading of CSV and JSON files.

This is a useful module for handling simple data science assignments.  It is not part
of the top-level module because it has not been fully tested.

:author:  Walker M. White
:version: July 17, 2018
"""


class FileToolError(Exception):
    """
    A simple error class to unify error responses for the filetools package.
    """
    pass


def read_txt(filename):
    """
    Reads the contents of the text file ``filename``.
    
    This function reads the contents of the file ``filename`` and returns the result.
    This function assumes the file is a text file and not a binary file.  If this is
    not the case, it will raise an error.
    
    :param filename: The file to read
    :type filename:  ``str``
    
    :return: A string representing the file contents
    :rtype:  ``str``
    """
    import json
    try:
        file = open(filename)
        data = file.read()
        file.close()
        return data
    except FileNotFoundError:
        message = 'Text file %s does not exist' % repr(filename)
    except Exception as e:
        message = 'Text file %s has error %s' % (repr(filename), str(e))
    
    raise FileToolError(message)


def read_json(filename):
    """
    Reads the contents of the JSON file ``filename``.
    
    This function reads the contents of the file ``filename``. Assuming it is a properly
    encoded JSON file, it will convert this into a Python data value, which will either
    be a dictionary or a list. 
    
    If the file does not exist, or is not a proper JSON file, this function will raise an 
    error.
    
    :param filename: The file to read
    :type filename:  ``str``
    
    :return: A dictionary or list representing the file contents
    :rtype:  ``dict`` or ``list``
    """
    import json
    try:
        file = open(filename)
        data = json.loads(file.read())
        file.close()
        return data
    except FileNotFoundError:
        message = 'JSON file %s does not exist' % repr(filename)
    except json.decoder.JSONDecodeError as e:
        message = str(e)
        pos = message.find(':')
        message = 'JSON file %s has an error at%s' % (repr(filename), message[pos+1:])
    except Exception as e:
        message = 'JSON file %s has error %s' % (repr(filename), str(e))
    
    raise FileToolError(message)


def read_csv(filename):
    """
    Reads the contents of the CSV file ``filename``.
    
    This function reads the contents of the file ``filename``. Assuming it is a properly
    encoded csv file, it will convert this into a 2-dimensional list, where each element
    of the list is the row.  Cells in the row are all interpreted as strings.  It is
    up to the programmer to interpret this data, since CSV files contain no type 
    information.
    
    If the file does not exist, or is not a proper CSV file, this function will raise an
    error.
    
    :param filename: The file to read
    :type filename:  ``str``
    
    :return: A two dimensional list including the header as the first row
    :rtype:  2d ``list``
    """
    try:
        file = open(filename)
        result = []
        header = _csv_split(file.readline())
        column = len(header)
        result.append(header)
        if column > 0:
            mismatch = None
            pos = 1
            for line in file:
                row = _csv_split(line)
                if not mismatch and len(row) != column:
                    mismatch = (pos,len(row))
                result.append(row)
                pos += 1
            if mismatch is None:
                file.close()
                return result
            message = 'CSV file %s has invalid row at %d' % (repr(filename),mismatch[0])
        else:
            message = 'CSV file %s is empty' % repr(filename)
        file.close()
    except FileNotFoundError:
        message = 'CSV file %s does not exist' % repr(filename)
    except Exception as e:
        message = e.args[0]
    raise FileToolError(message)


def read_package(folder):
    """
    Reads the contents of the given directory.
    
    A package is a directory with a file ``index.json`` inside of it.  This JSON is a
    one-level dictionary mapping keys to file names.  These files should all be in
    the directory.  Each file can be either a text , JSON, or CSV file, or another
    directory (which should also be a package).
    
    This method returns a dictionary maping the keys to the contents of each file,
    as defined recursively by :func:`read_text`, :func:`read_json`, :func:`read_csv`,
    and :func:`read_package`.
   
    Packages are mainly used as a way of gathering data files from multiple source.
    Any package can actually be represented as a single JSON file, but it is not 
    always easy to construct this file.
    
    If the directory does not exist, or is not a proper package, this function will raise
    an error.
    
    :param folder: The directory to read
    :type folder:  ``str``
    
    :return: A dictionary containing the contents of each file in the package
    :rtype: ``dict``
    """
    import os.path
    index = os.path.join(folder,'index.json')
    directory = read_json(index)
    
    result = {}
    for key in directory:
        path, ext = os.path.splitext(directory[key])
        full = os.path.join(folder,directory[key])
        if os.path.isdir(full):
            result[key] = read_package(full)
        elif ext in ['.txt', '']:
            result[key] = read_txt(full)
        elif ext == '.csv':
            result[key] = read_csv(full)
        elif ext == '.json':
            result[key] = read_json(full)
        else:
            raise FileToolError('Unrecognized file extension %s' % repr(ext))
    return result


def write_txt(data,filename):
    """
    Writes the given data out as a text file ``filename``.
    
    The data should be a string.  If it is not proper data, this function will raise
    an error.  The filename may have any extension.
    
    :param data: The text to write to a file
    :type data:  ``str``
    
    :param filename: The file to write
    :type filename:  ``str``
    """
    try:
        file = open(filename,'w')
        file.write(data)
        file.close()
        return
    except Exception as e:
        message = e.args[0]
    
    raise FileToolError(message)


def write_json(data,filename):
    """
    Writes the given data out as a JSON file ``filename``.
    
    The data should be an JSON encodable value (e.g. either a primitive -- int, float, 
    bool, string -- or a list or dictionary of JSON encodable values).  If it is not 
    proper data, this function will raise an error.
    
    The JSON filename must either have no extension, or the extension .json.  Any other
    extension will cause an error.
    
    :param data: The Python value to encode as a JSON
    :type data: JSON-encodable value
    
    :param filename: The file to write
    :type filename:  ``str``
    """
    try:
        import json
        import os.path
        prefix, ext = os.path.splitext(filename)
        valid = True
        message = ''
        if ext == '':
            filename += '.json'
        elif ext != '.json':
            message = '%s is not a valid JSON extension' % repr(ext)
        if not message:
            file = open(filename,'w')
            file.write(json.dumps(data,indent=4))
            file.close()
            return
    except TypeError as e:
        message = str(e)
    except PermissionError as e:
        message = e.strerror+': '+filename
    except Exception as e:
        message = e.args[0]
    
    raise FileToolError(message)


def write_csv(data,filename):
    """
    Writes the given data out as a CSV file ``filename``.
    
    To be a proper CSV file, it must be a 2-dimensional list with the first row 
    containing only strings.  All other rows may be any python value.  Dates are
    converted using isoformatting.  All other objects are converted to their string
    representation.
    
    The CSV filename must either have no extension, or the extension .csv.  Any other
    extension will cause an error.
    
    :param data: The Python value to encode as a CSV file
    :type data:  2d ``list``
    
    :param filename: The file to write
    :type filename:  ``str``
    """
    try:
        import os.path
        prefix, ext = os.path.splitext(filename)
        message = ''
        if ext == '':
            filename += '.csv'
        elif ext != '.csv':
            message = '%s is not a valid CSV extension' % repr(ext)
            valid = False
        
        if not message:
            message = _check_csv(data)
        
        if not message:
            file = open(filename,'w')
            for row in data:
                file.write(_csv_join(row))
            file.close()
            return
    except PermissionError as e:
        message = e.strerror+': '+filename
    except Exception as e:
        message = e.args[0]
    
    raise FileToolError(message)


pass
# #mark -
# #mark CSV Helpers
def _csv_split(line):
    """
    Returns a row a single line of a CSV file [INTERNAL FUNCTION]
    
    This function is better than the basic split() method because it takes into 
    account the quotation rules for CSV files.
    
    Parameter line: A line of a CSV file
    Precondition: line is a string
    """
    result = []
    inside = False
    left = 0
    for rght in range(len(line)):
        if not inside and line[rght] == ',':
            result.append(_dequote(line[left:rght]))
            left = rght+1
        elif line[rght] == '"':
            inside = not inside
    if line[-1] == '\n':
        remain = line[left:-1] # Remove line return
    else:
        remain = line[left:]
    result.append(_dequote(remain))
    return result


def _csv_join(row):
    """
    Returns single line of a CSV file from a list of values [INTERNAL FUNCTION]
    
    This function is better than the basic join() method because it takes into 
    account the quotation rules for CSV files. In addition, it converts of all the
    data into properly encoded strings.
    
    Parameter row: A row of values to encode
    Precondition: row is a list
    """
    return ','.join(map(_requote,row))+'\n'


def _dequote(text):
    """
    Returns the value ``text`` missing the external quotes [INTERNAL FUNCTION]
    
    External quotes are optional in CSV files. This function removes them, and properly
    transforms any internal (proper) quotes.
    
    If ``text`` has no external quotes, this function does nothing.
    
    Parameter text: A string to dequote
    Precondition: text is a string
    """
    if len(text) < 1:
        return text
    
    left = 1 if text[0] == '"' else 0
    rght = len(text)-1 if text[-1] == '"' else len(text)
    text = text[left:rght]
    return text.replace('""','"')


def _requote(value):
    """
    Returns the value as a string, quoted if necessary [INTERNAL FUNCTION]
    
    External quotes are optional in CSV files, but necessary if the value is a string
    containing either a quote or a comma.  This function searches for those values and
    quotes the result as necessary.
    
    Value does not need to be a string.  In that case, it will convert the string to
    a value.  If value is a date, it will use the isoformat() method.  Otherwise, the
    str() function is used.
    
    Parameter value: A value to convert
    Precondition: None
    """
    try:
        text = value.isoformat()
    except:
        text = str(value)
    
    if '"' in text or ',' in text:
        text = text.replace('"','""')
        return '"'+text+'"'
    return text


def _check_csv(data):
    """
    Returns a string representing an error message if data is malformed [INTERNAL FUNCTION]
    
    If the data is a properly formed CSV value, this function returns the empty string.
    
    Parameter data: The Python value to encode as a CSV file
    Precondition: None
    """
    from functools import reduce
    if type(data) not in [tuple,list]:
        return 'CSV data is neither a tuple nor a list'
    
    if not (type(data[0]) in [tuple,list] and reduce(lambda a,b: a and type(b) == str, data[0])):
        return 'Row %s is not a valid CSV header' % repr(data[0])
    
    headlen = len(data[0])
    for pos in range(1,len(data)):
        if type(data[pos]) not in [tuple,list]:
            return 'Row %d is malformed' %  pos
        elif len(data[pos]) != headlen:
            return 'Row %d does not match the header length' %  pos
    
    return ''

