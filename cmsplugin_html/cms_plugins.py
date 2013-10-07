from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.conf import settings
from django.utils.translation import ugettext as _
from .models import HTMLPlugin as HTMLPluginModel

####### HTML Plugin ###################


class HTMLPlugin(CMSPluginBase):
    model = HTMLPluginModel
    name = _("HTML")
    render_template = "cmsplugin_html/html_instance.djhtml"  # template to render the plugin with
    change_form_template = "cmsplugin_html/change_form.html"  # Template for the admin form
    admin_preview = False

    def replace_vars(self, input):
        return input.replace("{{STATIC_URL}}", settings.STATIC_URL)

    def render(self, context, instance, placeholder):
        context.update({
            'plugin_html': self.replace_vars(instance.html),
            'plugin_js':   self.replace_vars(instance.js),
            'plugin_css':  self.replace_vars(instance.css),
            })
        return context

plugin_pool.register_plugin(HTMLPlugin)
