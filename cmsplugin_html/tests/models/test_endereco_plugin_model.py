from test_tools.test import CMSPluginModelTestCase
from ..interface import models


EnderecoPluginModel = models.EnderecoPluginModel


class EnderecoPluginModelTest(CMSPluginModelTestCase):

    model = EnderecoPluginModel
    meta = {}
    campos = [
        {'nome': 'nome', 'field': 'CharField', "max_length": 30},
        {'nome': 'logradouro', 'field': 'CharField', "max_length": 26},
        {'nome': 'numero', 'field': 'PositiveSmallIntegerField'},
        {'nome': 'bairro', 'field': 'CharField', "max_length": 26},
        {'nome': 'cidade', 'field': 'CharField', "max_length": 26},
        {'nome': 'estado', 'field': 'CharField', "max_length": 2},
        {'nome': 'cep', 'field': 'CharField', "max_length": 9},
        {'nome': 'telefone', 'field': 'CharField', "max_length": 16},
        {'nome': 'email', 'field': 'EmailField'},
        {'nome': 'texto', 'field': 'TextField'},
    ]
