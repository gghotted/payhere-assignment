# Generated by Django 4.1.7 on 2023-02-26 15:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성 시간')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정 시간')),
                ('code', models.CharField(max_length=32, verbose_name='코드')),
                ('access_scope', models.CharField(max_length=255, verbose_name='접근 범위')),
                ('expired_at', models.DateTimeField(verbose_name='만료일')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guests', to=settings.AUTH_USER_MODEL, verbose_name='생성자')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]
