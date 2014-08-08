# coding: utf-8
from django.test import TestCase
from ..fields import PercentIntegerFormField, PercentIntegerField


class ItemTest(object):

    argumento = saida = excecao = None

    def __init__(self, argumento, saida=None, excecao=False):
        self.argumento = argumento

        if not excecao:
            self.saida = saida
        if not saida:
            self.excecao = excecao

        if not excecao and not saida:
            raise ValueError(
                'Defina apenas se existirá uma saida ou se deve ser'
                'lançado uma exceção')


class UpperCharFieldTest(TestCase):

    def test_form_field(self):
        from django.forms import ValidationError

        campo = PercentIntegerFormField()

        # FIXME: Estes testes devem ser habilitados quando a unidade % for
        # habilitada
        TEST_CASES = [
            # Testes de descoberta de unidade
            # ItemTest('10', '10%'),
            # ItemTest('100', '100%'),
            ItemTest('101', '101px'),
            ItemTest('200', '200px'),

            # Testes passando a unidade '%'
            # ItemTest('10%', '10%'),
            # ItemTest('100%', '100%'),

            # Testes passando a unidade 'px'
            ItemTest('10px', '10px'),
            ItemTest('200px', '200px'),

            # Testes que devem dar errado
            ItemTest('10.5px', excecao=True),
            ItemTest('10px%', excecao=True),
            ItemTest('10pxpx', excecao=True),
            ItemTest('10huehue', excecao=True),
            ItemTest('troll', excecao=True),
            ItemTest('tr100ll', excecao=True),
            ItemTest('10%', excecao=True),

        ]

        for test in TEST_CASES:

            if test.excecao:
                try:
                    campo.clean(test.argumento)
                except ValidationError:
                    pass
                else:
                    self.fail(
                        'Não foi chamado a excecao %s quando foi '
                        'chamado com o valor %s' % (
                            ValidationError, test.argumento
                        )
                    )
            else:
                self.assertEqual(campo.clean(test.argumento), test.saida)

    def test_model_field(self):
        field = PercentIntegerField()

        # Testes do max_length default e form default
        self.assertEqual(field.max_length, 6)
        self.assertTrue(isinstance(field.formfield(), PercentIntegerFormField))

        # Testes do To Python
        # self.assertEqual(field.to_python(50), '50%')
        self.assertEqual(field.to_python(500), '500px')
        self.assertEqual(field.to_python('50px'), '50px')
        # self.assertEqual(field.to_python('500%'), '500%')

        # Testes do Get Prep Value
        # self.assertEqual(field.get_prep_value(50), '50%')
        self.assertEqual(field.get_prep_value(500), '500px')
        self.assertEqual(field.get_prep_value('50px'), '50px')
        # self.assertEqual(field.get_prep_value('500%'), '500%')
