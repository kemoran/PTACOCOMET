# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PasaTurnos', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='encuesta',
            old_name='respuesta_encuesta',
            new_name='respuesta',
        ),
    ]
