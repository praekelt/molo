# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.core.management.sql import emit_pre_migrate_signal


class Migration(migrations.Migration):
    """
    Migration 34 needs migration 0040 from wagtail core
    and this Migration will run wagtail migration before
    molo core migration 34
    """
    def run_wagtail_migration_before_core_34(apps, schema_editor):
        db_alias = schema_editor.connection.alias
        emit_pre_migrate_signal(2, False, db_alias)

    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
        ('core', '0072_fb_tracking_id'),
        ('core', '0033_bannerindexpage_footerindexpage_sectionindexpage'),
    ]

    operations = [
        migrations.RunPython(run_wagtail_migration_before_core_34),
    ]
