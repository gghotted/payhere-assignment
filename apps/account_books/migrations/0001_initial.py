# Generated by Django 4.1.7 on 2023-02-26 02:10

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성 시간')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정 시간')),
                ('name', models.CharField(max_length=64, validators=[django.core.validators.MinLengthValidator(3), django.core.validators.MaxLengthValidator(20)], verbose_name='이름')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_books', to=settings.AUTH_USER_MODEL, verbose_name='유저')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]
