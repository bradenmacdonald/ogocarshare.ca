from compressor.filters import CompilerFilter
from django.conf import settings


class CssAutoprefixerFilter(CompilerFilter):
    command = settings.PROJECT_ROOT + "/node_modules/.bin/postcss --use autoprefixer --output {outfile} {infile}"


class SassFilter(CompilerFilter):
    command = settings.PROJECT_ROOT + "/node_modules/.bin/node-sass --output-style compressed {infile} {outfile}"
