# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-23 12:29
from __future__ import unicode_literals

from django.db import migrations
from django.core.management.sql import emit_post_migrate_signal


class Migration(migrations.Migration):
    def add_bulk_delete_permission_for_moderator_group(apps, schema_editor):
        db_alias = schema_editor.connection.alias
        try:
            # Django 1.9
            emit_post_migrate_signal(2, False, db_alias)
        except TypeError:
            # Django < 1.9
            try:
                # Django 1.8
                emit_post_migrate_signal(2, False, 'default', db_alias)
            except TypeError:  # Django < 1.8
                emit_post_migrate_signal([], 2, False, 'default', db_alias)

        Group = apps.get_model('auth.Group')
        Permission = apps.get_model('auth.Permission')
        GroupPagePermission = apps.get_model('wagtailcore.GroupPagePermission')
        SectionIndexPage = apps.get_model('core.SectionIndexPage')

        # <- Moderator ->
        moderator_group = Group.objects.filter(name='Moderators').first()
        if moderator_group:
            sections = SectionIndexPage.objects.first()
            GroupPagePermission.objects.get_or_create(
                group_id=moderator_group.id,
                page_id=sections.id,
                permission_type='bulk_delete'
            )


    dependencies = [
        ('core', '0051_remove_user_permission_for_moderator_group'),
        ('contenttypes', '__latest__'),
        ('wagtailcore', '__latest__'),
        ('wagtailadmin', '__latest__'),
        ('wagtailusers', '__latest__'),
        ('sites', '__latest__'),
        ('auth', '__latest__'),
    ]

    operations = [
        migrations.RunPython(add_bulk_delete_permission_for_moderator_group),
    ]
