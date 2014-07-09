from __future__ import absolute_import
from compressor.filters import CompilerFilter
from compressor.filters.css_default import CssAbsoluteFilter
from compressor.utils import staticfiles
from django.conf import settings


class CssAbsoluteFilterFixed(CssAbsoluteFilter):
    def find(self, basename):
        if basename and staticfiles.finders:
            return staticfiles.finders.find(basename)


class LessFilter(CompilerFilter):
    def __init__(self, content, attrs, **kwargs):
        cmd = settings.PROJECT_ROOT + "/node_modules/less/bin/lessc -x {infile} > {outfile}"
        super(LessFilter, self).__init__(content, command=cmd, **kwargs)
