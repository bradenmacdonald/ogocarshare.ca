from __future__ import division
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
#from django.contrib import admin
from django.utils.translation import ugettext as _
from .models import YouTubeVideo


class YouTubePlugin(CMSPluginBase):
    model = YouTubeVideo
    name = _("YouTube Video")
    render_template = "cmsplugin_youtube/instance.html"  # template to render the plugin with
    admin_preview = False
    fields = ("video_id", "autoplay", "hide_info", "light_theme")

    def render(self, context, instance, placeholder):
        context.update({
            'video_id': instance.video_id,
            'autoplay': instance.autoplay,
            'hide_info': instance.hide_info,
            'light_theme': instance.light_theme,
        })
        return context

plugin_pool.register_plugin(YouTubePlugin)
