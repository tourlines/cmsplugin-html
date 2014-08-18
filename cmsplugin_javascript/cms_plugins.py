# coding: utf-8
from cms.plugin_pool import plugin_pool
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from .models import CarouselPluginModel, GridPluginModel, ItemGridPluginModel

# FIXME/SEE: cmsplugin_javascript/tests/interface.py
try:
    from lib.cms_.djangocms.plugins.html.cmsplugin_html.cms_plugins import \
        BasePlugin
except ImportError:
    from cmsplugin_html.cms_plugins import BasePlugin


# Isto permite que o usuário cadastre novos grids e plugins para o grid de
# forma dinâmica, sempre definindo nestas constantes quais são os plugins que
# o mesmo criou
if 'CMSPLUGIN_GRID_ITENS' in dir(settings):
    GRID_ITENS = settings.CMSPLUGIN_GRID_ITENS
else:
    GRID_ITENS = []


if 'CMSPLUGIN_GRIDS' in dir(settings):
    GRIDS = settings.CMSPLUGIN_GRIDS
else:
    GRIDS = []


class CarouselPlugin(BasePlugin):

    model = CarouselPluginModel
    name = _('Carousel')
    render_template = 'cmsplugin_javascript/carousel.html'
    allow_children = True
    child_classes = ['FilerImagePlugin']


class GridPlugin(BasePlugin):

    model = GridPluginModel
    name = _('Grid')
    render_template = 'cmsplugin_javascript/grid.html'
    allow_children = True
    child_classes = ['ItemGridPlugin'] + GRID_ITENS

    def render(self, context, instance, placeholder):
        retorno = \
            super(GridPlugin, self).render(context, instance, placeholder)

        paginas, plugins_invalidos = instance.get_paginas_grid()

        retorno.update({
            # Páginas é uma relação de sliders e plugins que deve aparecer
            # em cada slide
            'paginas': paginas,
            'plugins_invalidos': plugins_invalidos,
            # Dentro de itens deve ter todas as informações referente aos
            # mesmos como a altura e largura de cada um deles
            'itens': {
                'altura': instance.get_altura_itens(),
                'largura': instance.get_largura_itens()
            }
        })
        return retorno


class ItemGridPlugin(BasePlugin):

    model = ItemGridPluginModel
    name = ('Grid Item')
    render_template = 'cmsplugin_javascript/grid_itens/base.html'
    exclude = ('status',)
    require_parent = True
    parent_classes = ['GridPlugin'] + GRIDS


plugin_pool.register_plugin(CarouselPlugin)
plugin_pool.register_plugin(GridPlugin)
plugin_pool.register_plugin(ItemGridPlugin)
