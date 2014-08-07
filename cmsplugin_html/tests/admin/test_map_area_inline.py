# coding: utf-8
from django.test import TestCase
from ..interface import models, admin


MapAreaInlineAdmin = admin.MapAreaInlineAdmin
AreaTagModel = models.AreaTagModel


class MapAreaInlineAdminTest(TestCase):

    admin = MapAreaInlineAdmin
    model = AreaTagModel

    def test_validacao_admin(self):
        self.assertEqual(self.admin.model, self.model)
        self.assertEqual(self.admin.fk_name, 'mapa')
