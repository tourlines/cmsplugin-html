# coding: utf-8
from cms.exceptions import PluginAlreadyRegistered
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from .admin import MapAreaInlineAdmin
from .models import EnderecoPluginModel, MapPluginModel


class BasePlugin(CMSPluginBase):

    module = _('Elementos Básicos')

    def render(self, context, instance, placeholder):
        context.update({'instance': instance})
        return context


class EnderecoPlugin(BasePlugin):
    model = EnderecoPluginModel
    name = _('Endereço')
    render_template = 'cmsplugin_html/endereco.html'


class MapPlugin(BasePlugin):
    model = MapPluginModel
    name = _('Imagem Mapeada')
    render_template = 'cmsplugin_html/map.html'
    inlines = (MapAreaInlineAdmin,)

    def render(self, context, instance, placeholder):
        retorno = super(MapPlugin, self).render(context, instance, placeholder)
        retorno.update({'areas': instance.areatagmodel_set.all()})
        return retorno


# A todo momento que este arquivo é importado ele tenta registrar estes plugins
# procedimento que gera erro pois o django cms já carregou os mesmos
try:
    plugin_pool.register_plugin(EnderecoPlugin)
    plugin_pool.register_plugin(MapPlugin)
except PluginAlreadyRegistered:
    pass
