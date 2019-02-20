# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-02-17 16:59
from __future__ import unicode_literals

import aesthetic_computation.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aesthetic_computation', '0003_auto_20190217_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image_460px',
            field=models.ImageField(default='okreplalcethis', upload_to=aesthetic_computation.models.upload_path),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='image_large',
            field=models.ImageField(default='replacethisalso', upload_to=''),
            preserve_default=False,
        ),
    ]