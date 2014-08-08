# coding: utf-8
from .base import PluginBaseTest
from django.utils.translation import ugettext_lazy as _


class GridPluginTest(PluginBaseTest):
    plugin = 'ItemGridPlugin'
    validar_local_template = False

    atributos = {
        'name': _('Grid Item'),
        'exclude': ('status',),
        'render_template': 'cmsplugin_javascript/grid_itens/base.html',
        'require_parent': True,
        'parent_classes': ['GridPlugin']
    }
