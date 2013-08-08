from __future__ import absolute_import
from datetime import date
from filer.utils.files import get_valid_filename
import os.path


def filer_namer(inst, filename):
    "Organize files into folders based on year only"
    return os.path.join(u"{}".format(date.today().year - 2000), get_valid_filename(filename))
