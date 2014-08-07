# coding: utf-8
from .base import PluginBaseTest
from django.utils.translation import ugettext_lazy as _


class EnderecoPluginTest(PluginBaseTest):

    plugin = 'EnderecoPlugin'

    atributos = {
        'name': _("Endereço"),
    }
