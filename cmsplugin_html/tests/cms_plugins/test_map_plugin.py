# coding: utf-8
from .base import PluginBaseTest
from django.utils.translation import ugettext_lazy as _
from ..interface import models


MapPluginModel = models.MapPluginModel


class MapPluginTest(PluginBaseTest):

    plugin = 'MapPlugin'
    validar_nome_model = False

    atributos = {
        'model': MapPluginModel,
        'name': _("Imagem Mapeada")
    }
