# coding: utf-8


def gen_filer_image_field():
    import os
    from django.core.files import File
    from filer.models import Image
    from filer.models.foldermodels import Folder

    DUMMY_IMAGE_DIR = os.path.dirname(__file__)
    DUMMY_IMAGE_NAME_VERBOSE = 'Mommy Image'
    DUMMY_IMAGE_NAME = 'mommy.png'
    FOLDER_NAME = 'mommy'

    return Image.objects.create(
        name=DUMMY_IMAGE_NAME_VERBOSE,
        original_filename=DUMMY_IMAGE_NAME,
        folder=Folder.objects.get_or_create(name=FOLDER_NAME)[0],
        file=File(open(
            os.path.join(DUMMY_IMAGE_DIR, DUMMY_IMAGE_NAME)),
            name=DUMMY_IMAGE_NAME)
    )


def gen_comma_separated_integer_field(max_length):
    import random

    retorno = ''
    for item in range(max_length / 2):
        retorno = '%s,%s' % (retorno, random.randint(0, 9))

    return retorno


gen_comma_separated_integer_field.required = ['max_length']
