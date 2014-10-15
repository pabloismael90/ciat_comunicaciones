# -*- coding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User
from thumbs_logo import ImageWithThumbsField
from utils import *
from ckeditor.fields import RichTextField
from contrapartes.models import Pais

# Create your models here.
# 
class Aliados(models.Model):
    nombre = models.CharField(max_length=200)
    siglas = models.CharField("Siglas o nombre corto",help_text="Siglas o nombre corto de la oganización",max_length=200,blank=True, null=True)
    logo = ImageWithThumbsField(upload_to=get_file_path,
                                   sizes=((350,250), (70,60),(180,160)), 
                                   null=True, blank=True)
    fileDir = 'aliados/logos/'
    pais = models.ForeignKey(Pais)
    fundacion = models.CharField('Año de fundación', max_length=200, 
                                 blank=True, null=True)
    temas = RichTextField(blank=True, null=True)
    generalidades = RichTextField(blank=True, null=True)
    contacto = models.CharField(max_length=200,blank=True, null=True)
    telefono = models.CharField(max_length=200, blank=True, null=True)
    sitio_web = models.URLField(blank=True, null=True)
    rss = models.CharField(max_length=200,blank=True, null=True)

    class Meta:
        verbose_name_plural = "Aliados"
        unique_together = ("nombre",)

    def __unicode__(self):
        return self.nombre

    def get_absolute_url(self):
        return '/aliados/%d/' % (self.id,)
