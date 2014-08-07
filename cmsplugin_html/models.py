# coding: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models import CMSPlugin
from filer.fields.image import FilerImageField


class EnderecoPluginModel(CMSPlugin):

    nome = models.CharField(max_length=30)
    logradouro = models.CharField(max_length=26)
    numero = models.PositiveSmallIntegerField()
    bairro = models.CharField(max_length=26)
    cidade = models.CharField(max_length=26)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=9)
    telefone = models.CharField(max_length=16)
    email = models.EmailField()
    texto = models.TextField()

    def __unicode__(self):
        return u'%s' % self.nome


class MapPluginModel(CMSPlugin):

    imagem = FilerImageField(null=False, blank=False)
    usar_tooltip = models.BooleanField(
        help_text=(
            'Por padrão o plugin cria apenas uma área clicável na imagem, '
            'caso deseje que aparece a texto de descrição quando o usuário '
            'passar o mouse em cima da área habilite este opção.'),
        default=False, blank=True, verbose_name='exibir mensagem')

    def copy_relations(self, oldinstance):
        for item in oldinstance.areatagmodel_set.all():
            item.pk = item.id = None
            item.mapa = self
            item.save()


class AreaTagModel(CMSPlugin):

    class Shapes:
        DEFAULT = 'default'
        RECT = 'rect'
        CIRCLE = 'circle'
        POLY = 'poly'

    SHAPES_CHOICES = (
        (Shapes.DEFAULT, _('Padrão')),
        (Shapes.RECT, _('Retângulo')),
        (Shapes.CIRCLE, _('Círculo')),
        (Shapes.POLY, _('Polígono')),
    )

    shape = models.CharField(choices=SHAPES_CHOICES, max_length=7)
    coords = models.CommaSeparatedIntegerField(max_length=80)
    url = models.CharField(max_length=100)
    mapa = models.ForeignKey(MapPluginModel)
    mensagem = models.TextField(null=True, blank=True)
