# coding: utf-8
from django.utils.translation import ugettext_lazy as _
from model_mommy import mommy
from test_tools.test import ModelTestCase
from ..interface import models, consts, fields


GridPluginModel = models.GridPluginModel
ItemGridPluginModel = models.ItemGridPluginModel


class GridPluginTest(ModelTestCase):

    model = GridPluginModel
    meta = {}
    campos = [
        {
            'nome': 'titulo', 'field': 'CharField', 'max_length': 40,
            'blank': True, 'null': True
        }, {
            'nome': 'colunas', 'field': 'PositiveSmallIntegerField'
        }, {
            'nome': 'itens_pagina', 'field': 'PositiveSmallIntegerField'
        }, {
            'nome': 'altura', 'field': fields.PercentIntegerField,
            'null': True, 'blank': True
        }, {
            'nome': 'largura', 'field': fields.PercentIntegerField
        }, {
            'nome': 'velocidade', 'field': 'PositiveSmallIntegerField',
            'blank': True, 'default': consts.DEFAULT_TRANSITION_INTERVAL
        }
    ]

    def test_get_altura_itens(self):
        """
        Testa se a função retorna a largura dos itens corretamente
        """
        # FIXME: Testes devem ser habilidatos quando for usar o '%' como
        # unidade do campo
        # obj = mommy.make(GridPluginModel, colunas=2, itens_pagina=4)
        # self.assertEqual(obj.get_altura_itens(), None)

        # obj = mommy.make(
        #     GridPluginModel, colunas=4, itens_pagina=4, altura='50%')
        # self.assertEqual(obj.get_altura_itens(), '50%')

        obj = mommy.make(
            GridPluginModel, colunas=4, itens_pagina=5, altura='500px')
        self.assertEqual(obj.get_altura_itens(), '250px')

    def test_get_largura_itens(self):
        """
        Testa se a função retorna a largura dos itens corretamente
        """
        # FIXME: Testes devem ser habilidatos quando for usar o '%' como
        # unidade do campo
        # obj = mommy.make(GridPluginModel, colunas=2, itens_pagina=4)
        # self.assertEqual(obj.get_largura_itens(), '50%')

        # obj = mommy.make(GridPluginModel, colunas=4, itens_pagina=4)
        # self.assertEqual(obj.get_largura_itens(), '25%')

        obj = mommy.make(
            GridPluginModel, colunas=4, itens_pagina=4, largura='500px')
        self.assertEqual(obj.get_largura_itens(), '125px')

    def test_get_paginas_grid(self):
        """
        Testa se o objeto esta organizando corretamente os itens
        (plugins filhos) nas páginas
        """
        from datetime import date, timedelta

        obj = mommy.make(GridPluginModel, colunas=2, itens_pagina=4)

        self.assertEqual(len(obj.get_paginas_grid()), 0)

        child_plugin_validos = [
            mommy.make(ItemGridPluginModel),
            mommy.make(ItemGridPluginModel),
            mommy.make(ItemGridPluginModel),
            mommy.make(ItemGridPluginModel),

            mommy.make(ItemGridPluginModel),
            mommy.make(ItemGridPluginModel),
            mommy.make(ItemGridPluginModel),
            mommy.make(ItemGridPluginModel),

            mommy.make(ItemGridPluginModel),
        ]
        child_plugin_invalidos = [
            mommy.make(
                ItemGridPluginModel,
                dt_inicio=date.today() - timedelta(days=2),
                dt_fim=date.today() - timedelta(days=1)
            )
        ]

        obj.child_plugin_instances = \
            child_plugin_validos + child_plugin_invalidos

        esperado = [4, 4, 1]

        retorno = obj.get_paginas_grid()
        # Garante que possui a mesma quantidade de páginas
        self.assertEqual(len(esperado), len(retorno))

        # Garante que cada página possui a quantidade de itens corretos
        for elementos, elementos_esperados in zip(retorno, esperado):
            self.assertEqual(len(elementos), elementos_esperados)

        # Garente que a função não mandou para o limbo nenhum elemento
        objetos_retornados = []
        for lista in retorno:
            for elemento in lista:
                objetos_retornados.append(elemento)
        self.assertItemsEqual(child_plugin_validos, objetos_retornados)




