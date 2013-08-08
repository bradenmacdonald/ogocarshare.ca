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
    """
    CssAbsoluteFilter is sometimes not getting called when DEBUG=False
    This affects any CSS files outside of the ogo/static/ directory,
    resulting in missing images on the production site.
    """
    def __init__(self, content, attrs, **kwargs):
        cmd = settings.PROJECT_ROOT + "/node_modules/recess/bin/" + "recess --compile --compress {infile} > {outfile}"
        super(LessFilter, self).__init__(content, command=cmd, **kwargs)

    def input(self, **kwargs):
        content = super(LessFilter, self).input(**kwargs)
        return content  # CssAbsoluteFilterFixed(content).input(**kwargs)
