# coding: utf-8
from test_tools.test import CMSPluginModelTestCase
from filer.fields.image import FilerImageField
from model_mommy import mommy
from ..interface import models


MapPluginModel = models.MapPluginModel
AreaTagModel = models.AreaTagModel


class MapPluginModelTest(CMSPluginModelTestCase):

    model = MapPluginModel
    meta = {}
    campos = [
        {
            'nome': 'imagem', 'field': FilerImageField
        }, {
            'nome': 'usar_tooltip', 'field': 'BooleanField', 'blank': True,
            'default': False, 'verbose_name': True, 'help_text': True
        },
    ]

    def test_copy_relations(self):
        """
        O django CMS tem uma particularidde quanto a plugins com
        ForeignKeys. Para poder criar o ambiente de rascunho e
        produção na hora de criar páginas o cms duplica todos os
        elementos (plugins, placeholders) linkados a página, um para
        o rascunho e outro para produção. E por este motivo é preciso
        implementar uma função que copia as relações de um plugin
        (apenas quando ele possui ForeignKey).

        Esta função testa se após criar um plugin novo e chamarmos a
        função copy_relations padrão do django cms o novo plugin
        vai possuir as relações do antigo
        """
        mapa = mommy.make(MapPluginModel)
        novo_mapa = mommy.make(MapPluginModel)
        mapa_areas = [
            mommy.make(AreaTagModel, mapa=mapa),
            mommy.make(AreaTagModel, mapa=mapa)
        ]

        self.assertFalse(novo_mapa.areatagmodel_set.all().count())

        novo_mapa.copy_relations(mapa)

        self.assertEqual(
            novo_mapa.areatagmodel_set.all().count(), len(mapa_areas))
