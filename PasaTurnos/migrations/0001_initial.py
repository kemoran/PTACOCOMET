# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import PasaTurnos.models
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cajero',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=45L, validators=[PasaTurnos.models.ValidarNombre])),
                ('apellido', models.CharField(max_length=45L, validators=[PasaTurnos.models.ValidarNombre])),
                ('dui', models.CharField(max_length=10L, validators=[PasaTurnos.models.ValidarDUI])),
                ('nit', models.CharField(max_length=17L, validators=[PasaTurnos.models.ValidarNIT])),
                ('genero', models.CharField(max_length=1L, choices=[('M', 'Masculino'), ('F', 'Femenino')])),
                ('telefono', models.CharField(max_length=9L, validators=[PasaTurnos.models.ValidarTelefono])),
                ('correo_electronico', models.CharField(max_length=50L, validators=[django.core.validators.EmailValidator()])),
            ],
            options={
                'db_table': 'cajero',
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=45L, validators=[PasaTurnos.models.ValidarNombre])),
                ('apellido', models.CharField(max_length=45L, validators=[PasaTurnos.models.ValidarNombre])),
                ('dui', models.CharField(max_length=10L, validators=[PasaTurnos.models.ValidarDUI])),
                ('genero', models.CharField(max_length=1L, choices=[('M', 'Masculino'), ('F', 'Femenino')])),
                ('fecha_nacimiento', models.DateField()),
                ('telefono', models.CharField(blank=True, max_length=9L, validators=[PasaTurnos.models.ValidarTelefono])),
                ('correo_electronico', models.CharField(blank=True, max_length=50L, validators=[django.core.validators.EmailValidator()])),
            ],
            options={
                'db_table': 'cliente',
            },
        ),
        migrations.CreateModel(
            name='Ejecutivo',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=45L, validators=[PasaTurnos.models.ValidarNombre])),
                ('apellido', models.CharField(max_length=45L, validators=[PasaTurnos.models.ValidarNombre])),
                ('dui', models.CharField(max_length=10L, validators=[PasaTurnos.models.ValidarDUI])),
                ('nit', models.CharField(max_length=17L, validators=[PasaTurnos.models.ValidarNIT])),
                ('genero', models.CharField(max_length=1L, choices=[('M', 'Masculino'), ('F', 'Femenino')])),
                ('telefono', models.CharField(max_length=9L, validators=[PasaTurnos.models.ValidarTelefono])),
                ('correo_electronico', models.CharField(max_length=50L, validators=[django.core.validators.EmailValidator()])),
            ],
            options={
                'db_table': 'ejecutivo',
            },
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=45L)),
                ('numero_registro', models.CharField(blank=True, max_length=45L, validators=[PasaTurnos.models.ValidarNRC])),
                ('telefono', models.CharField(max_length=9L, validators=[PasaTurnos.models.ValidarTelefono])),
                ('fax', models.CharField(blank=True, max_length=9L, validators=[PasaTurnos.models.ValidarTelefono])),
                ('direccion', models.CharField(max_length=100L)),
                ('correo_electronico', models.CharField(blank=True, max_length=50L, validators=[django.core.validators.EmailValidator()])),
                ('sitio_web', models.CharField(max_length=50L, blank=True)),
            ],
            options={
                'db_table': 'empresa',
            },
        ),
        migrations.CreateModel(
            name='Encuesta',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('respuesta_encuesta', models.CharField(max_length=2L, choices=[('M', 'Malo'), ('B', 'Bueno'), ('MB', 'Muy Bueno')])),
                ('fecha_emicion', models.DateTimeField()),
            ],
            options={
                'db_table': 'encuesta',
            },
        ),
        migrations.CreateModel(
            name='Gerente',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=45L, validators=[PasaTurnos.models.ValidarNombre])),
                ('apellido', models.CharField(max_length=45L, validators=[PasaTurnos.models.ValidarNombre])),
                ('dui', models.CharField(max_length=10L, validators=[PasaTurnos.models.ValidarDUI])),
                ('nit', models.CharField(max_length=17L, validators=[PasaTurnos.models.ValidarNIT])),
                ('genero', models.CharField(max_length=1L, choices=[('M', 'Masculino'), ('F', 'Femenino')])),
                ('telefono', models.CharField(max_length=9L, validators=[PasaTurnos.models.ValidarTelefono])),
                ('correo_electronico', models.CharField(max_length=50L, validators=[django.core.validators.EmailValidator()])),
                ('empresa_id', models.ForeignKey(to='PasaTurnos.Empresa', db_column='empresa_id')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
                'db_table': 'gerente',
            },
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('descripcion', models.CharField(max_length=45L)),
            ],
            options={
                'db_table': 'servicio',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('numero', models.CharField(max_length=10L)),
                ('fecha_emicion', models.DateTimeField()),
                ('estado', models.CharField(max_length=1L)),
                ('cliente_id', models.ForeignKey(to='PasaTurnos.Cliente', db_column='cliente_id')),
                ('servicio_id', models.ForeignKey(to='PasaTurnos.Servicio', db_column='servicio_id')),
            ],
            options={
                'db_table': 'ticket',
            },
        ),
        migrations.CreateModel(
            name='TipoAtencion',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('descripcion', models.CharField(max_length=45L)),
            ],
            options={
                'db_table': 'tipo_atencion',
            },
        ),
        migrations.CreateModel(
            name='Ventanilla',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('descripcion', models.CharField(max_length=45L)),
                ('tipo_atencion_id', models.ForeignKey(to='PasaTurnos.TipoAtencion', db_column='tipo_atencion_id')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
                'db_table': 'ventanilla',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('descripcion', models.CharField(max_length=50L)),
                ('ruta', PasaTurnos.models.FileInputPersonalizado(null=True, upload_to='VideosPublicitarios', blank=True)),
            ],
            options={
                'db_table': 'video',
            },
        ),
        migrations.AddField(
            model_name='ticket',
            name='ventanilla_id',
            field=models.ForeignKey(db_column='ventanilla_id', to='PasaTurnos.Ventanilla', null=True),
        ),
        migrations.AddField(
            model_name='servicio',
            name='tipo_atencion_id',
            field=models.ForeignKey(to='PasaTurnos.TipoAtencion', db_column='tipo_atencion_id'),
        ),
        migrations.AddField(
            model_name='ejecutivo',
            name='empresa_id',
            field=models.ForeignKey(to='PasaTurnos.Empresa', db_column='empresa_id'),
        ),
        migrations.AddField(
            model_name='ejecutivo',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True),
        ),
        migrations.AddField(
            model_name='cajero',
            name='empresa_id',
            field=models.ForeignKey(to='PasaTurnos.Empresa', db_column='empresa_id'),
        ),
        migrations.AddField(
            model_name='cajero',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]
