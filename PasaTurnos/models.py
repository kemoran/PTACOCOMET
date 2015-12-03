# -*- encoding: utf-8 -*-

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Clase para agregar validaciones a los modelos
from django.core.exceptions import ValidationError
from django.core import validators
# Clase para evaluar expresiones regulares
import re

# Validaciones personalizadas
def ValidarDUI(value):
    if re.match("^\d{8}-\d{1}$", value) == None:
        raise ValidationError(u'%s DUI Incorrecto' % value)

'''
def ValidarNombre(value):
    if re.match("^[a-zA-Z]+ [a-zA-Z]+$", value) == None:
        raise ValidationError(u'%s Dato Incorrecto' % value)
'''

def ValidarNombre(value):
    if (re.match("^[a-zA-z]+$", value) != None or re.match("^([a-zA-z]+\s[a-zA-z]+)$", value) != None) == False:
        raise ValidationError(u'%s Dato Incorrecto' % value)

def ValidarLetra(value):
    if re.match("^[a-zA-Z]+$", value) == None:
        raise ValidationError(u'%s Dato Incorrecto' % value)

def ValidarNumero(value):
    if re.match("^\d+$", value) == None:
        raise ValidationError(u'%s Dato Incorrecto' % value)

def ValidarNIT(value):
    if re.match("^\d{4}-\d{6}-\d{3}-\d{1}$", value) == None:
        raise ValidationError(u'%s NIT Incorrecto' % value)

def ValidarTelefono(value):
    if re.match("^\d{4}-\d{4}$", value) == None:
        raise ValidationError(u'%s Numero de Telefono Incorrecto' % value)

def ValidarNRC(value):
    if re.match("^\d{5}-\d{1}$", value) == None:
        raise ValidationError(u'%s Numero de Registro Incorrecto' % value)

def ValidarCorreo(value):
    if re.match("^\w+@\w+\.\S+$", value) == None:
        raise ValidationError(u'%s Correo Incorrecto' % value)

# Fin validaciones personalizadas

# Elecciones para genero
GENERO = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        )

# Elecciones para encuesta
ENCUESTA = (
        ('M', 'Malo'),
        ('B', 'Bueno'),
        ('MB', 'Muy Bueno'),
        )

""" CAMPO PERSONALIZADO PARA FILEINPUT """
# FileField personalizado
from django.db.models import FileField
from django.forms import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _

class FileInputPersonalizado(FileField):
    def __init__(self, content_types=None, max_upload_size=None, **kwargs):
        self.content_types = content_types
        self.max_upload_size = max_upload_size
        
        super(FileInputPersonalizado, self).__init__(**kwargs)
        
    def clean(self, *args, **kwargs):
        data = super(FileInputPersonalizado, self).clean(*args, **kwargs)

        file = data.file
        try:
            content_type = file.content_type
            if content_type in self.content_types:
                if file._size > self.max_upload_size:
                    raise forms.ValidationError(_('Tamaño maximo soportado: %s. Tamaño actual del archivo %s') % (filesizeformat(self.max_upload_size), filesizeformat(file._size)))
            else:
                raise forms.ValidationError(_('Tipo de formato no soportado.'))
        except AttributeError:
            pass

        return data
#---------------------------------------------------

class Empresa(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45L)
    numero_registro = models.CharField(max_length=45L, blank=True, validators=[ValidarNRC])
    telefono = models.CharField(max_length=9L, validators=[ValidarTelefono])
    fax = models.CharField(max_length=9L, blank=True, validators=[ValidarTelefono])
    direccion = models.CharField(max_length=100L)
    correo_electronico = models.CharField(max_length=50L, blank=True, validators=[validators.validate_email])
    sitio_web = models.CharField(max_length=50L, blank=True)
    class Meta:
        db_table = 'empresa'

class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45L, validators=[ValidarNombre])
    apellido = models.CharField(max_length=45L, validators=[ValidarNombre])
    dui = models.CharField(max_length=10L, validators=[ValidarDUI])
    genero = models.CharField(max_length=1L, choices=GENERO)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=9L, blank=True, validators=[ValidarTelefono])
    correo_electronico = models.CharField(max_length=50L, blank=True, validators=[validators.validate_email])
    class Meta:
        db_table = 'cliente'

class TipoAtencion(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=45L)
    class Meta:
        db_table = 'tipo_atencion'

class Servicio(models.Model):
    id = models.AutoField(primary_key=True)
    tipo_atencion_id = models.ForeignKey(TipoAtencion, db_column='tipo_atencion_id', on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=45L)
    class Meta:
        db_table = 'servicio'

class Ventanilla(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)
    tipo_atencion_id = models.ForeignKey(TipoAtencion, db_column='tipo_atencion_id', on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=45L)
    class Meta:
        db_table = 'ventanilla'

class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    cliente_id = models.ForeignKey(Cliente, db_column='cliente_id', on_delete=models.CASCADE)
    ventanilla_id = models.ForeignKey(Ventanilla, db_column='ventanilla_id', null=True, on_delete=models.CASCADE)
    servicio_id = models.ForeignKey(Servicio, db_column='servicio_id', on_delete=models.CASCADE)
    numero = models.CharField(max_length=10L)
    fecha_emicion = models.DateTimeField()
    estado = models.CharField(max_length=1L) # E: Espera, P: Proceso, A: Atendido, N: Anulado
    class Meta:
        db_table = 'ticket'

class Cajero(models.Model):
    id = models.AutoField(primary_key=True)
    empresa_id = models.ForeignKey(Empresa, db_column='empresa_id', on_delete=models.CASCADE)
    user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=45L, validators=[ValidarNombre])
    apellido = models.CharField(max_length=45L, validators=[ValidarNombre])
    dui = models.CharField(max_length=10L, validators=[ValidarDUI])
    nit = models.CharField(max_length=17L, validators=[ValidarNIT])
    genero = models.CharField(max_length=1L, choices=GENERO)
    telefono = models.CharField(max_length=9L, validators=[ValidarTelefono])
    correo_electronico = models.CharField(max_length=50L, validators=[validators.validate_email])
    class Meta:
        db_table = 'cajero'

class Ejecutivo(models.Model):
    id = models.AutoField(primary_key=True)
    empresa_id = models.ForeignKey(Empresa, db_column='empresa_id', on_delete=models.CASCADE)
    user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=45L, validators=[ValidarNombre])
    apellido = models.CharField(max_length=45L, validators=[ValidarNombre])
    dui = models.CharField(max_length=10L, validators=[ValidarDUI])
    nit = models.CharField(max_length=17L, validators=[ValidarNIT])
    genero = models.CharField(max_length=1L, choices=GENERO)
    telefono = models.CharField(max_length=9L, validators=[ValidarTelefono])
    correo_electronico = models.CharField(max_length=50L, validators=[validators.validate_email])
    class Meta:
        db_table = 'ejecutivo'

class Gerente(models.Model):
    id = models.AutoField(primary_key=True)
    empresa_id = models.ForeignKey(Empresa, db_column='empresa_id', on_delete=models.CASCADE)
    user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=45L, validators=[ValidarNombre])
    apellido = models.CharField(max_length=45L, validators=[ValidarNombre])
    dui = models.CharField(max_length=10L, validators=[ValidarDUI])
    nit = models.CharField(max_length=17L, validators=[ValidarNIT])
    genero = models.CharField(max_length=1L, choices=GENERO)
    telefono = models.CharField(max_length=9L, validators=[ValidarTelefono])
    correo_electronico = models.CharField(max_length=50L, validators=[validators.validate_email])
    class Meta:
        db_table = 'gerente'

class Encuesta(models.Model):
    id = models.AutoField(primary_key=True)
    respuesta = models.CharField(max_length=2L, choices=ENCUESTA)
    fecha_emicion = models.DateTimeField()
    class Meta:
        db_table ='encuesta'

class Video(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50L)
    ruta = FileInputPersonalizado(blank=True, null=True, upload_to='VideosPublicitarios', content_types=['video/webm'], max_upload_size=429916160)
    class Meta:
        db_table = 'video'