# coding: utf-8
from django.utils.translation import ugettext_lazy as _
from model_mommy import mommy
from .base import PluginBaseTest
from ..interface import models


class GridPluginTest(PluginBaseTest):
    plugin = 'GridPlugin'

    atributos = {
        'name': _('Grid'),
        'allow_children': True,
        'child_classes': ['ItemGridPlugin'],
    }

    def test_render_key_paginas(self):
        ItemGridPluginModel = models.ItemGridPluginModel

        obj_plugin = self.get_plugin()()
        instance = mommy.make(obj_plugin.model, itens_pagina=4)

        # Aqui é feito um teste sem areas no mapa e por isto espera-se um
        # retorno vazio
        contexto = obj_plugin.render({}, instance, None)

        self.assertIn('paginas', contexto)
        self.assertTrue(isinstance(contexto['paginas'], list))
        self.assertEqual(len(contexto['paginas']), 0)

        # Agora é criado vários itens, e apenas algums estão linkados ao plugin
        # NOTA: Se criar mais que 4 plugins filhos terá que alterar o valor
        # do atributo itens_pagina usado para instanciar o objeto, caso
        # contrario o teste irá falhar!
        instance.child_plugin_instances = [
            mommy.make(ItemGridPluginModel),
            mommy.make(ItemGridPluginModel),
            mommy.make(ItemGridPluginModel)
        ]
        instance.save()
        mommy.make(ItemGridPluginModel)
        mommy.make(ItemGridPluginModel)

        contexto = obj_plugin.render({}, instance, None)
        self.assertIn('paginas', contexto)
        self.assertTrue(isinstance(contexto['paginas'], list))
        self.assertItemsEqual(
            contexto['paginas'][0], instance.child_plugin_instances)

    def test_render_key_itens(self):
        obj_plugin = self.get_plugin()()
        instance = mommy.make(obj_plugin.model)
        contexto = obj_plugin.render({}, instance, None)

        self.assertEqual(
            contexto['itens']['altura'], instance.get_altura_itens())
        self.assertEqual(
            contexto['itens']['largura'], instance.get_largura_itens())
