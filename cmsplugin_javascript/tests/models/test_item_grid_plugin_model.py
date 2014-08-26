# coding: utf-8
from django.utils.translation import ugettext_lazy as _
from model_mommy import mommy
from test_tools.test import ModelTestCase
from ..interface import models


ItemGridPluginModel = models.ItemGridPluginModel


class ItemGridTest(ModelTestCase):

    model = ItemGridPluginModel
    meta = {}
    atributos = [
        {
            'nome': 'url', 'field': 'CharField', 'max_length': 200
        }, {
            'nome': 'target', 'field': 'CharField', 'max_length': 9,
            'default': ItemGridPluginModel.Targets.SELF, 'choices': (
                ['blank', '_blank (Nova Página)'],
                ['self', '_self (Mesma Página)'],
                ['parent', '_parent (Frame - Frameset pai)'],
                ['top', '_top (Frame - Página Inteira)'],
                ['framename', 'framename (Frame - Nome)'])
        }, {
            'nome': 'titulo', 'field': 'CharField', 'max_length': 100
        }, {
            'nome': 'descricao', 'field': 'TextField'
        }, {
            'nome': 'dt_inicio', 'field': 'DateField', 'null': True,
            'blank': True, 'verbose_name': _('data início')
        }, {
            'nome': 'dt_fim', 'field': 'DateField', 'null': True,
            'blank': True, 'verbose_name': _('data fim')
        }, {
            'nome': 'status', 'field': 'PositiveSmallIntegerField',
            'blank': True, 'null': False, 'editable': False,
            'default': ItemGridPluginModel.Status.VALIDO,
            'choices': (
                ['valido', 'válido'],
                'expirado',
                ['pre_cadastro', 'pré-cadastro'])
        },
    ]

    def test_datas(self):
        """
        Testa a funcionalidade dos atributos relacionados a data

        O campo dt_inicio e dt_fim existem para possibilitar que o
        usuário coloque um período de válidade a um determinado item.
        Estes dois atributos possuem algumas peculiaridades, São elas:
            - Data de Fim não pode ser maior que a de Inicio;
            - Caso não esteja passado da data de fim o item é válido;
            - Quando a data de fim é null o item expira;
            - Quando ambas são nulas o item sempŕe será válido.
        """
        from datetime import date, timedelta
        from django.core.exceptions import ValidationError

        VALIDO = self.model.Status.VALIDO
        EXPIRADO = self.model.Status.EXPIRADO
        PRE_CADASTRO = self.model.Status.PRE_CADASTRO

        hoje = date.today()
        amanha = date.today() + timedelta(days=1)
        ontem = date.today() - timedelta(days=1)

        class ItemTest(object):

            def __init__(self, dt_inicio, dt_fim, status=None, excecao=False):
                self.dt_inicio = dt_inicio
                self.dt_fim = dt_fim
                self.status = status
                self.excecao = excecao

        TEST_CASES = [
            ItemTest(dt_inicio=None, dt_fim=None, status=VALIDO),
            ItemTest(dt_inicio=None, dt_fim=hoje, status=VALIDO),
            ItemTest(dt_inicio=None, dt_fim=ontem, status=EXPIRADO),
            ItemTest(dt_inicio=None, dt_fim=amanha, status=VALIDO),

            ItemTest(dt_inicio=hoje, dt_fim=None, status=VALIDO),
            ItemTest(dt_inicio=hoje, dt_fim=hoje, status=VALIDO),
            ItemTest(dt_inicio=hoje, dt_fim=ontem, excecao=True),
            ItemTest(dt_inicio=hoje, dt_fim=amanha, status=VALIDO),

            ItemTest(dt_inicio=ontem, dt_fim=None, status=VALIDO),
            ItemTest(dt_inicio=ontem, dt_fim=hoje, status=VALIDO),
            ItemTest(dt_inicio=ontem, dt_fim=ontem, status=EXPIRADO),
            ItemTest(dt_inicio=ontem, dt_fim=amanha, status=VALIDO),

            ItemTest(dt_inicio=amanha, dt_fim=None, status=PRE_CADASTRO),
            ItemTest(dt_inicio=amanha, dt_fim=hoje, excecao=True),
            ItemTest(dt_inicio=amanha, dt_fim=ontem, excecao=True),
            ItemTest(dt_inicio=amanha, dt_fim=amanha, status=PRE_CADASTRO),
        ]

        for test_case in TEST_CASES:
            try:
                obj = mommy.make(
                    self.model,
                    dt_inicio=test_case.dt_inicio, dt_fim=test_case.dt_fim)
            except ValidationError as e:
                if test_case.excecao:
                    continue
                raise e

            if test_case.status == VALIDO:
                self.assertTrue(obj.esta_valido())
            else:
                self.assertFalse(obj.esta_valido())

            # A comparação é feita usando um objeto no banco, para garantir que
            # o status foi salvo no objeto
            obj_banco = self.model.objects.get(
                url=obj.url,
                target=obj.target,
                titulo=obj.titulo,
                descricao=obj.descricao,
                dt_inicio=obj.dt_inicio,
                dt_fim=obj.dt_fim,
                status=obj.status,
            )

            relacao = dict(self.model.STATUS_CHOICES)
            self.assertEqual(obj_banco.status, test_case.status, (
                'O status do item não foi modificado após a validação.\n'
                'Data Inicio: %s, Data Fim: %s\n'
                'Esperado: %s, Retornado: %s'
            ) % (
                test_case.dt_inicio, test_case.dt_fim,
                relacao[test_case.status], relacao[obj_banco.status]
            ))
            obj_banco.delete()

    def test_max_largura_e_altura(self):
        # TODO: Em um futuro proximo a biblioteca abaixo se unirá com esta
        # FIXME: Este será o unico teste que DEVE falhar pelo fato de não ser
        # possivel importar esta biblioteca de dentro da app ainda
        from lib.cms_.djangocms.api import ItemStaticPlaceholder, ItemPlugin

        argumentos = {
            'url': '#',
            'titulo': 'unittest',
            'descricao': self.__class__.__name__
        }

        ItemStaticPlaceholder('unittest', plugins=[
            ItemPlugin(
                'GridPlugin', {
                    'colunas': 3, 'itens_pagina': 6, 'largura': '600px',
                    'altura': '400px'
                }, filhos=[
                    ItemPlugin('ItemGridPlugin', argumentos)
                ]
            ),
        ]).criar()

        item_grid = ItemGridPluginModel.objects.filter(**argumentos)[0]

        self.assertEqual(item_grid.get_max_largura(), '200px')
        self.assertEqual(item_grid.get_max_altura(), '200px')

    def test_unicode(self):
        plugin = mommy.make(ItemGridPluginModel)

        self.assertEqual(plugin.__unicode__(), '%s | Status: %s' % (
            plugin.titulo,
            dict(ItemGridPluginModel.STATUS_CHOICES)[plugin.status]))
