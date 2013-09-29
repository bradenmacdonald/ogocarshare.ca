from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models import CMSPlugin


#def _cms_plugin_youtube_upload_to(inst, orig_filename):
#    from django.template.defaultfilters import slugify
#    ext = orig_filename.lower().rsplit('.',1)[-1]
#    if ext not in ("jpg", "png", "jpeg", "gif"):
#        ext = "img"
#    return "yt-covers/{}.{}".format(slugify(inst.name), ext)

class YouTubeVideo(CMSPlugin):

    video_id = models.CharField(max_length=12)
    autoplay = models.BooleanField(null=False, default=False)
    hide_info = models.BooleanField(null=False, default=False, help_text=_("Don't display the title and uploader before the video starts."))
    light_theme = models.BooleanField(null=False, default=False)
    #cover = models.ImageField(null=False, blank=False, upload_to=_cms_plugin_youtube_upload_to, width_field='logo_w', height_field='logo_h')

    def __unicode__(self):
        return self.video_id
