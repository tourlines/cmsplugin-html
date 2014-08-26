# coding: utf-8
from django.utils.translation import ugettext_lazy as _
from .base import CMSPluginTestCase


class EnderecoPluginTest(CMSPluginTestCase):

    plugin = 'EnderecoPlugin'

    atributos = {
        'name': _("Endereço"),
    }
