# coding: utf-8
from django.contrib import admin
from .models import AreaTagModel


class MapAreaInlineAdmin(admin.TabularInline):
    model = AreaTagModel
    fk_name = 'mapa'
