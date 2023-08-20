import re
import os
import shutil
import distutils.dir_util as dirutil
from tkinter import Tk, filedialog

__all__ = [
    'sep',
	'current',
	'isdir',
	'isfile',
	'join',
	'basename',
	'dirname',
    'abspath',
	'name',
	'ext',
	'exist',
	'rename',
	'delete',
	'copy',
	'move',
	'write',
	'read',
	'delete_content',
    'walk',
	'listdir',
	'getmtime',
	'split',
	'select_path',
]

def sep():
    return os.sep

def current():
    return os.getcwd()

def isdir(path):
    return os.path.isdir(path)

def isfile(path):
    return os.path.isfile(path)

def join(*paths):
    return os.path.join(*paths)

def basename(path):
    return os.path.basename(path)

def dirname(path):
    return os.path.dirname(path)

def abspath(path):
    return os.path.abspath(path)

def name(path):
    return os.path.splitext(os.path.split(path)[1])[0]

def ext(path):
    return os.path.splitext(path)[1]

def exist(path):
    return os.path.exists(path)

def rename(source, dest):
    os.rename(source, dest)

def delete(url):
    if isfile(url):
        os.remove(url)
    elif isdir(url):
        shutil.rmtree(url)

def copy(source, dest, replace=True):
    if exist(dest) and replace:
        delete(dest)
    if not exist(dest):
        if isdir(source):
            dirutil.copy_tree(source, dest)
        elif isfile(source):
            shutil.copy(source, dest)
    else:
        raise FileExistsError("{} already exist".format(dest))

def move(source, dest, replace=True):
    if replace or (not replace and not exist(dest)):
        copy(source, dest)
        delete(source)
    else:
        raise FileExistsError("{} already exist".format(dest))

def write(url, content=None, mode='w'):
    with open(url, mode) as fp:
        return fp.write(content)

def read(url, type='str'):
    with open(url, 'r') as c:
        if type == 'str':
            return c.read()
        elif type == 'list':
            return c.readlines()

def delete_content(path):
    for (root,dirs,files) in os.walk(path):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            shutil.rmtree(os.path.join(root, dir))

def walk(path, type=None, start=None, end=None, contain=None, style='name', regex=None):
    ret = dict()
    for p, dirs, files in os.walk(path):
        ret[p] = listdir(p, type, start, end, contain, style, regex)
    return ret

def listdir(path, type=None, start=None, end=None, contain=None, style='name', regex=None):
    if type not in ['file', 'dir', None]:
        raise TypeError("'type' argument can only be 'None', 'file' or 'dir'")
    str_arguments = dict(
        path=path,
        start=start,
        end=end,
        contain=contain,
        style=style,
        regex=regex
    )
    for key, value in str_arguments.items():
        if value and not isinstance(value, str):
            raise TypeError("'{}' argument can only be a string".format(key))
    if style not in [None, 'name', 'path']:
        raise TypeError("'style' argument can only be 'None', 'name' or 'path'")
    ret = []
    for element in os.listdir(path):
        ok = True
        if type == 'file' and not isfile(join(path, element)):
            ok = False
        if type == 'dir' and not isdir(join(path, element)):
            ok = False
        if start and not element.startswith(start):
            ok = False
        if end and not element.endswith(end):
            ok = False
        if contain and contain not in element:
            ok = False
        if regex and not re.match(regex, element):
            ok = False
        if ok:
            element = dict(name=element, path=os.path.join(path, element))
            if style:
                ret.append(element[style])
            else:
                ret.append(element)
    return ret

def isempty(path: str):
    elements = '{} is not a valid path'.format(path)
    if exist(path):
        if isdir(path):
            elements = [element for element in listdir(path)]
        if isfile(path):
            elements = read(path, type='list')
    if isinstance(elements, str):
        raise TypeError(elements)
    return True if elements else False

def getmtime(path):
    return os.path.getmtime(path)

def split(path):
    return os.path.split(path)

def select_path(type='file', title = None):
	root = Tk()
	root.withdraw()
	try: path = filedialog.askopenfilename(parent=root, title=title) if type == 'file' else filedialog.askdirectory(parent=root, title=title)
	except: path = ''
	finally: root.destroy()
	return path if path else None








