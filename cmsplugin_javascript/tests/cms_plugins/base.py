# coding: utf-8
from ..interface import test_base


class PluginBaseTest(test_base.PluginBaseTest):

    def get_plugin(self):
        from ..interface import cms_plugins

        return self.get_plugin_(cms_plugins)
