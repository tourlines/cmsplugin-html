# coding: utf-8
from test_tools.test import CMSPluginTestCase


class CMSPluginTestCase(CMSPluginTestCase):

    def get_plugin(self):
        from ..interface import cms_plugins
        return self.get_plugin_(cms_plugins)
