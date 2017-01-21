# pylint: disable=abstract-method
"""
Helper classes used to build OGO's theme assets with django-compressor
"""
from compressor.filters import CompilerFilter
from django.conf import settings


class CssAutoprefixerFilter(CompilerFilter):
    """
    Filter to pipe CSS through autoprefixer

    autoprefixer adds vendor prefixes to rules where needed.
    """
    command = settings.PROJECT_ROOT + "/node_modules/.bin/postcss --use autoprefixer --output {outfile} {infile}"


class SassFilter(CompilerFilter):
    """
    Compile SASS using LibSass
    """
    command = settings.PROJECT_ROOT + "/node_modules/.bin/node-sass --output-style compressed {infile} {outfile}"
