# coding: utf-8
from test_tools.test import CMSPluginModelTestCase
from ..interface import models


CarouselPluginModel = models.CarouselPluginModel


class EnderecoPluginModelTest(CMSPluginModelTestCase):

    model = CarouselPluginModel
    meta = {}
    campos = [
        {
            'nome': 'indicador', 'field': 'BooleanField', 'help_text': True,
            'verbose_name': True, 'default': True
        }, {
            'nome': 'largura', 'field': 'PositiveSmallIntegerField',
            'help_text': True, 'null': True, 'blank': True
        }, {
            'nome': 'velocidade', 'field': 'PositiveSmallIntegerField',
            'help_text': True, 'blank': True, 'default': 6000
        },
    ]
