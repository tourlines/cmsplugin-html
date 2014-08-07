# coding: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models import CMSPlugin


class CarouselPluginModel(CMSPlugin):

    indicador = models.BooleanField(
        help_text=(_(
            'Se irá aparecer as "bolinhas" que permite o usuário avançar/'
            'recuar sliders'
        )), verbose_name='paginação', default=True)
    altura = models.PositiveSmallIntegerField(
        help_text=_('Altura do carousel, em pixels'), blank=True, null=True)
    largura = models.PositiveSmallIntegerField(
        help_text=_('Largura do carousel, em pixels'), blank=True, null=True)
    velocidade = models.PositiveSmallIntegerField(
        help_text=_('Tempo entre a transição de slides, em milissegundos'),
        default=6000, blank=True)
