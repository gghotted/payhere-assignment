# Generated by Django 4.1.7 on 2023-03-05 17:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("share", "0002_alter_guest_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="guest",
            name="object_pks",
            field=models.JSONField(blank=True, default="", verbose_name="객체 pks"),
            preserve_default=False,
        ),
    ]
