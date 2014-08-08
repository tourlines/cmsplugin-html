# coding: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models import CMSPlugin
from filer.fields.image import FilerImageField
from .consts import DEFAULT_TRANSITION_INTERVAL
from .fields import PercentIntegerField


class CarouselPluginModel(CMSPlugin):

    indicador = models.BooleanField(
        help_text=_(
            'Se irá aparecer as "bolinhas" que permite o usuário avançar/'
            'recuar sliders'
        ), verbose_name=_('paginação'), default=True)
    altura = models.PositiveSmallIntegerField(
        help_text=_('Altura do carousel, em pixels'), blank=True, null=True)
    largura = models.PositiveSmallIntegerField(
        help_text=_('Largura do carousel, em pixels'), blank=True, null=True)
    velocidade = models.PositiveSmallIntegerField(
        help_text=_('Tempo entre a transição de slides, em milissegundos'),
        default=DEFAULT_TRANSITION_INTERVAL, blank=True)


class GridPluginModel(CMSPlugin):

    titulo = models.CharField(max_length=40, blank=True, null=True)
    imagem_titulo = FilerImageField(blank=True, null=True)
    colunas = models.PositiveSmallIntegerField()
    itens_pagina = models.PositiveSmallIntegerField()
    altura = PercentIntegerField(null=True, blank=True)
    largura = PercentIntegerField()
    velocidade = models.PositiveSmallIntegerField(
        blank=True,
        default=DEFAULT_TRANSITION_INTERVAL)

    def get_valor_sem_unidade(self, valor):
        """
        Retorna a parte inteira de um valor sem a sua unidade
        """
        import re

        return int(valor[:re.search(r'[\D]', valor).start()])

    def get_unidade(self, valor):
        """
        Extrai e retorna apenas a unidade de um determinado valor
        """
        import re

        return valor[re.search(r'[\D]', valor).start():]

    def get_altura_itens(self):
        """
        Retorna a altura dos itens filhos junto com sua unidade
        """
        retorno = None

        if self.altura:
            linhas = self.itens_pagina / self.colunas
            # Para caso de quantidade de itens quebradas, ex. Col: 2, Item: 3
            # precisa ter 2 linhas
            if linhas != float(self.itens_pagina) / self.colunas:
                linhas += 1

            retorno = '%s%s' % (
                (self.get_valor_sem_unidade(self.altura) / linhas),
                self.get_unidade(self.altura))

        return retorno

    def get_largura_itens(self):
        """
        Retorna a largura dos itens filhos junto com sua unidade
        """
        return '%s%s' % (
            (self.get_valor_sem_unidade(self.largura) / self.colunas),
            self.get_unidade(self.largura))

    def get_paginas_grid(self):
        """
        Retorna uma lista de paginas com seus respectivos plugins

        Esta relação são os sliders do plugin, a lista contém várias
        outras listas filhas (cada lista é considerada como página) e
        dentro destas sub-listas possui vários plugins. Que são os
        plugins que devem aparecer naquela página.

        A quantidade de páginas é obtida usando a quantidade de
        colunas e itens_pagina e os plugins são organizados de forma
        aleatoria dentro da página.

        ALERT: Aparece na saída somente os plugins que estão validos
        """
        retorno = []
        if self.child_plugin_instances:
            plugins_validos = []
            for plugin in self.child_plugin_instances:
                # É possivel que o usuário faça bugs no sistema do django CMS
                # EX: criar um plugin e apertar F5, o resultado disto é um
                # plugin "fantasma" cadastrado no template sem nenhum atributo.
                # maiorias das vezes estes "plugins fantasmas" são criados
                # como uma instância do CMSPlugin (talvez pelo fato de não ter
                # restrição de atributos e por isto podem ser instanciados).
                # Esta linha irá evitar com que tentemos renderizar estes seres
                if not isinstance(plugin, ItemGridPluginModel):
                    continue

                if plugin.esta_valido():
                    plugins_validos.append(plugin)

            qtd_plugins = len(plugins_validos)
            numero_paginas = qtd_plugins / self.itens_pagina

            if numero_paginas != (float(qtd_plugins) / self.itens_pagina):
                numero_paginas += 1

            for pagina in range(numero_paginas):
                inicio = pagina * self.itens_pagina
                fim = (pagina + 1) * self.itens_pagina
                retorno.append(plugins_validos[inicio:fim])

        return retorno


class ItemGridPluginModel(CMSPlugin):

    class Targets:
        BLANK = '_blank'
        SELF = '_self'
        PARENT = '_parent'
        TOP = '_top'
        FRAMENAME = 'framename'

    TARGETS_CHOICES = (
        (Targets.BLANK, '_blank (Nova Página)'),
        (Targets.SELF, '_self (Mesma Página)'),
        (Targets.PARENT, '_parent (Frame - Frameset pai)'),
        (Targets.TOP, '_top (Frame - Página Inteira)'),
        (Targets.FRAMENAME, 'framename (Frame - Nome)'),
    )

    class Status:
        VALIDO = 1
        EXPIRADO = 2
        PRE_CADASTRO = 3

    STATUS_CHOICES = (
        (Status.VALIDO, 'válido'),
        (Status.EXPIRADO, 'expirado'),
        (Status.PRE_CADASTRO, 'pré-cadastro'),
    )

    url = models.CharField(max_length=200)
    target = models.CharField(
        max_length=9, choices=TARGETS_CHOICES, default=Targets.SELF)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    dt_inicio = models.DateField(
        null=True, blank=True, verbose_name=_('data início'))
    dt_fim = models.DateField(
        null=True, blank=True, verbose_name=_('data fim'))
    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES, blank=True, default=Status.VALIDO,
        editable=False)

    def validar_atributos(self, *args, **kwargs):
        """
        Validação semantica dos atributos do model
        """
        from django.core.exceptions import ValidationError

        if self.dt_inicio and self.dt_fim and self.dt_fim < self.dt_inicio:
            raise ValidationError(
                _('A data de fim não pode ser menor que a de inicio'))
        return True

    def save(self, *args, **kwargs):
        self.validar_atributos()
        super(ItemGridPluginModel, self).save(*args, **kwargs)

    def esta_valido(self):
        """
        Retorna se o item esta valido (no prazo) ou não (True/False)

        ALERT: Caso o item esteja expirado ele irá atualizar o status
        do item
        """
        from datetime import date

        hoje = date.today()
        retorno = False

        # Caso esteja expirado, não é preciso fazer validações. Caso o usuário
        # mude a data este dado é zerado e portanto se esta como expirado o
        # usuário não mudou a data
        if self.status == ItemGridPluginModel.Status.EXPIRADO:
            pass
        elif self.dt_fim and hoje > self.dt_fim:
            if self.status != ItemGridPluginModel.Status.EXPIRADO:
                self.status = ItemGridPluginModel.Status.EXPIRADO
                self.save()
            pass
        # Apenas coloca o status como um pré-cadastro, caso já não esteja
        elif self.dt_inicio and hoje < self.dt_inicio:
            if self.status != ItemGridPluginModel.Status.PRE_CADASTRO:
                self.status = ItemGridPluginModel.Status.PRE_CADASTRO
                self.save()

            pass
        # A data é válida quando o usuário não define uma data para expiração/
        # inicio, quando não tem inicio e não passou da data de fim. Quando
        # não tem data de fim, mas estamos após a data de inicio ou quando
        # estamos entre a data de inicio e fim
        elif (not self.dt_inicio and not self.dt_fim) or \
                (not self.dt_inicio and hoje <= self.dt_fim) or \
                (not self.dt_fim and hoje >= self.dt_inicio) or \
                (hoje >= self.dt_inicio and hoje <= self.dt_fim):

            if self.status != ItemGridPluginModel.Status.VALIDO:
                self.status = ItemGridPluginModel.Status.VALIDO
                self.save()

            retorno = True

        return retorno

    def get_max_largura(self):
        """
        Retorna qual é a largura máxima que o item pode ter
        """
        return self.parent.get_plugin_instance()[0].get_largura_itens()

    def get_max_altura(self):
        """
        Retorna qual é a altura máxima que o item pode ter
        """
        return self.parent.get_plugin_instance()[0].get_altura_itens()
