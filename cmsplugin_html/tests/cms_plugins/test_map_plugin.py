# coding: utf-8
from .base import PluginBaseTest
from django.utils.translation import ugettext_lazy as _
from model_mommy import mommy
from ..interface import models


MapPluginModel = models.MapPluginModel


class MapPluginTest(PluginBaseTest):

    plugin = 'MapPlugin'
    validar_nome_model = False

    atributos = {
        'model': MapPluginModel,
        'name': _("Imagem Mapeada")
    }

    def test_render(self):
        """
        Verifica se o render retornou as areas da imagem mapeada
        """
        from django.db.models.query import QuerySet

        AreaTagModel = models.AreaTagModel

        obj_plugin = self.get_plugin()()
        instance = mommy.make(obj_plugin.model)
        instance.save()

        # Aqui é feito um teste sem areas no mapa e por isto espera-se um
        # retorno vazio
        contexto = obj_plugin.render({}, instance, None)
        self.assertIn('areas', contexto)
        self.assertTrue(isinstance(contexto['areas'], QuerySet))
        self.assertEqual(contexto['areas'].count(), 0)

        # Agora é criado várias areas, e apenas algumas são do proprio mapa e
        # é esperado que no final apenas estas sejam retornadas
        mommy.make(AreaTagModel),
        mommy.make(AreaTagModel),
        areas = [
            mommy.make(AreaTagModel, mapa=instance),
            mommy.make(AreaTagModel, mapa=instance),
            mommy.make(AreaTagModel, mapa=instance),
        ]

        contexto = obj_plugin.render({}, instance, None)
        self.assertIn('areas', contexto)
        self.assertTrue(isinstance(contexto['areas'], QuerySet))
        self.assertItemsEqual(contexto['areas'], areas)
