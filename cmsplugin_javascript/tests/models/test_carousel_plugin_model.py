# coding: utf-8
from django.utils.translation import ugettext_lazy as _
from test_tools.test import CMSPluginModelTestCase
from ..interface import models


CarouselPluginModel = models.CarouselPluginModel


class EnderecoPluginModelTest(CMSPluginModelTestCase):

    model = CarouselPluginModel
    meta = {}
    atributos = [
        {
            'nome': 'indicador', 'field': 'BooleanField', 'help_text': True,
            'verbose_name': _('paginação'), 'default': True
        }, {
            'nome': 'largura', 'field': 'PositiveSmallIntegerField',
            'help_text': True, 'null': True, 'blank': True
        }, {
            'nome': 'velocidade', 'field': 'PositiveSmallIntegerField',
            'help_text': True, 'blank': True, 'default': 6000
        },
    ]
