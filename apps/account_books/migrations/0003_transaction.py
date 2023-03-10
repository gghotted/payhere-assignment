# Generated by Django 4.1.7 on 2023-02-26 10:10

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account_books', '0002_alter_accountbook_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성 시간')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정 시간')),
                ('description', models.TextField(verbose_name='설명')),
                ('occurred_at', models.DateTimeField(verbose_name='발생일')),
                ('amount', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='금액')),
                ('type', models.CharField(choices=[('+', '수입'), ('-', '지출')], max_length=1, verbose_name='거래 유형')),
                ('account_book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='account_books.accountbook', verbose_name='가계부')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]
