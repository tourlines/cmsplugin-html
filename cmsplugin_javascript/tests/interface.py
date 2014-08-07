# coding: utf-8
# FIXME: Atualmente não foi pensado em uma estrutura perfeita para trabalhar
# com bibliotecas externas e por isto para fazer estes testes funcionarem
# ao mesmo tempo como uma biblioteca externa e uma interna do nosso projeto
# é preciso fazer estas verificações na importação dos modulos.

# Existem algumas ideias de como solucionar estes problemas que ainda não
# foram aplicadas. A mais comum é: os projetos possuem uma pasta onde ficam as
# bibliotecas externas usadas, e alguns adicionam ela no path assim como o
# site-packages (afinal esta pasta trabalha como um). Atualmente esta ideia não
# funciona muito pois estruturamos nossas biblotecas em subpastas
try:
    from cms_.djangocms.plugins.html.cmsplugin_html.tests.cms_plugins import \
        base as test_base
    from cms_.djangocms.plugins.html.cmsplugin_javascript import models
    from cms_.djangocms.plugins.html.cmsplugin_javascript import \
        cms_plugins
except ImportError:
    from cmsplugin_javascript import models
    from cmsplugin_javascript import cms_plugins
