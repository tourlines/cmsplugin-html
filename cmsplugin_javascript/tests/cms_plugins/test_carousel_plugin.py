# coding: utf-8
from django.utils.translation import ugettext_lazy as _
from .base import CMSPluginTestCase


class CarouselPluginTest(CMSPluginTestCase):

    plugin = 'CarouselPlugin'
    atributos = {
        'name': _('Carousel'),
        'allow_children': True,
        'child_classes': ['FilerImagePlugin']
    }
