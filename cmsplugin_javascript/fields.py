# coding: utf-8
from django import forms
from django.db import models
from django.utils.translation import ugettext as _
from south.modelsinspector import add_introspection_rules
try:
    from lib.django_.db.model_mommy_ import mommy_ as mommy
except:
    mommy = None


UNIDADE_DEFAULT = 'px'
UNIDADES = [UNIDADE_DEFAULT]


def get_valor_validado(valor):
    import re

    MSG_ERROS = {
        'tipo': _('Este campo aceita apenas números inteiros'),
        'extensao': _(
            'Este campo aceita apenas a(s) unidade(s): pixels (px)'),
    }

    if not valor:
        return None

    if isinstance(valor, int):
        valor = '%s' % valor

    # Adiciona uma unidade (UNIDADE_DEFAULT) caso o valor esteja sem nenhuma
    try:
        unidade = valor[re.search(r'[\D]', valor).start():]
    except AttributeError:
        valor = '%s%s' % (valor, UNIDADE_DEFAULT)
        unidade = UNIDADE_DEFAULT

    # Aqui é feito uma verificação se a unidade é uma válida, primeiro verifica
    # se ela é uma unidade aceita, depois se não existe mais nenhum valor após
    # a mesma e por ultimo se não existe ela mais de uma vez
    if not unidade in UNIDADES or \
            not valor.split(unidade)[1] == '' or len(valor.split(unidade)) > 2:
        raise forms.ValidationError(MSG_ERROS['extensao'])

    # Verifica se o valor informado realmente é um inteiro
    try:
        valor_inteiro = int(valor.split(unidade)[0])
    except ValueError:
        raise ValueError(MSG_ERROS['tipo'])

    if valor_inteiro != float(valor.split(unidade)[0]):
        raise ValueError(MSG_ERROS['tipo'])

    return valor


class PercentIntegerFormField(forms.CharField):

    def clean(self, value):
        value = get_valor_validado(value)
        return super(PercentIntegerFormField, self).clean(value)


class PercentIntegerField(models.CharField):

    def __init__(self, *args, **kwargs):
        if not kwargs.get('max_length'):
            kwargs['max_length'] = 6
        super(PercentIntegerField, self).__init__(*args, **kwargs)

    def formfield(self, *args, **kwargs):
        defaults = {
            'form_class': PercentIntegerFormField,
        }
        defaults.update(kwargs)
        return super(PercentIntegerField, self).formfield(**defaults)

    def to_python(self, value):
        if value is None:
            return value
        else:
            return get_valor_validado(value)

    def get_prep_value(self, value):
        return self.to_python(value)


def gen_percent_integer(max_length):
    from random import randint

    valor = randint(0, int('9' * (int(max_length) - 2)))
    unidade = UNIDADES[randint(0, len(UNIDADES) - 1)]
    return '%s%s' % (valor, unidade)


gen_percent_integer.required = ['max_length']


if mommy:
    mommy.registrar(PercentIntegerField, gen_percent_integer)

add_introspection_rules([], ["^(.*)PercentIntegerField"])
