"""
OGO's customizations of Django Filer
"""
import os.path
from datetime import date

from filer.utils.files import get_valid_filename


def filer_namer(_inst, filename):
    """ Organize files into folders based on year only """
    return os.path.join("{}".format(date.today().year - 2000), get_valid_filename(filename))
