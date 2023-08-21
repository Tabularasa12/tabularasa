import os
import shutil
from importlib import import_module
from inspect import signature
from sys import path as syspath
from functools import wraps
from datetime import datetime
from flask import Blueprint, Flask, render_template, Markup, send_from_directory

from settings import DEFAUT_TEMPLATE
from utils.files import *
from utils.regex import REGEX
from utils.html.ressources.taggers import Tagger

def callize(obj):
    if callable(obj):
        return obj()
    return obj

def labelize(text=""):
    text=str(text)
    if "_" in text:
        text=" ".join(text.split("_"))
    return str(text).capitalize()

def inspect(funct, *param):
    return dict(name = funct.__name__, signature = [p.strip() for p in str(signature(funct))[1:-1].split(",")], args = [*param])

def clean_py_path(path):
    path = abspath(path)
    for _path, dirs, files in os.walk(path):
        for element in dirs+files:
            element = join(_path, element)
            if isdir(element) and (element.endswith('__pycache__') or element.endswith('.service') or element.startswith('.vscode')):
                shutil.rmtree(element)
            if isfile(element):
                if element.endswith('.pyc') or element.startswith('.goutput'):
                    os.remove(element)

def control_path_necessaries(base_path, necessaries):
    def is_necessary(path):
        path_split = path.strip(sep()).split(sep())
        path_str = f'{sep()}'
        error = ''
        for element in path_split:
            path_str = join(path_str, element)
            if '.' in element:
                if not isfile(path_str):
                    error = f'{path_str} is a necessary file but is not present in app path'
            else:
                if not isdir(path_str):
                    error = f'{path_str} is necessary folder but is not present in app path'
        return error

    for name, element in necessaries.items():
        error = is_necessary(join(base_path, element))
        if error:
            raise ModuleNotFoundError(error)
    return True

def add_syspath(path):
    if not path in syspath:
        syspath.append(path)
