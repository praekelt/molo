# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-07-27 09:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0062_increase_char_length_reaction_success'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticlePageLanguageProxy',
            fields=[
            ],
            options={
                'verbose_name': 'Article View',
                'proxy': True,
                'verbose_name_plural': 'Article View',
            },
            bases=('core.articlepage',),
        ),
    ]
