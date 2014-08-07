# coding: utf-8
from django.utils.translation import ugettext_lazy as _
from .base import PluginBaseTest


class CarouselPluginTest(PluginBaseTest):

    plugin = 'CarouselPlugin'
    atributos = {
        'name': _('Carousel'),
        'allow_children': True,
        'child_classes': ['FilerImagePlugin']
    }
