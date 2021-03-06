# Generated by Django 3.1.4 on 2020-12-15 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_auto_20201208_0615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='article_ordering_within_section',
            field=models.TextField(blank=True, choices=[('1', 'CMS Default Sorting'), ('2', 'First Published At'), ('3', 'First Published At Desc'), ('4', 'Primary Key'), ('5', 'Primary Key Desc')], default=None, help_text='Ordering of articles within a section', null=True),
        ),
    ]
