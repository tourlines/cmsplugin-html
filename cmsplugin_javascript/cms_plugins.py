# coding: utf-8
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from .models import CarouselPluginModel

try:
    from lib.cms_.djangocms.plugins.html.cmsplugin_html.cms_plugins import \
        BasePlugin
except ImportError:
    from cmsplugin_html.cms_plugin import BasePlugin


class CarouselPlugin(BasePlugin):
    model = CarouselPluginModel
    name = _("Carousel")
    render_template = 'cmsplugin_javascript/carousel.html'
    allow_children = True
    child_classes = ['FilerImagePlugin']


plugin_pool.register_plugin(CarouselPlugin)
