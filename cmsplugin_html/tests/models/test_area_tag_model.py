# coding: utf-8
from test_tools.test import CMSPluginModelTestCase
from ..interface import models


MapPluginModel = models.MapPluginModel
AreaTagModel = models.AreaTagModel


class AreaTagModelTest(CMSPluginModelTestCase):

    model = AreaTagModel
    meta = {}
    atributos = [
        {
            'nome': 'shape', 'field': 'CharField', 'max_length': 7,
            'choices': (
                ['default', 'Padrão'], ['rect', 'Retângulo'],
                ['circle', 'Círculo'], ['poly', 'Polígono'])
        }, {
            'nome': 'coords', 'field': 'CommaSeparatedIntegerField',
            'max_length': 80
        }, {
            'nome': 'url', 'field': 'CharField', 'max_length': 100
        }, {
            'nome': 'mapa', 'field': 'ForeignKey',
            'model': MapPluginModel
        }, {
            'nome': 'mensagem', 'field': 'TextField', 'null': True,
            'blank': True
        },
    ]
