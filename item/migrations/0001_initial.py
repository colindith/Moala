# Generated by Django 2.1.2 on 2018-12-08 03:38

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='none', max_length=40)),
                ('type', models.IntegerField(choices=[(0, 'Undefined'), (1, 'Seed'), (2, 'Resource'), (3, 'Kit'), (4, 'fruit')], default=0)),
                ('store_price', models.IntegerField(default=2)),
                ('sold_price', models.IntegerField(default=1)),
                ('values', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ItemPrototype',
            fields=[
                ('name', models.CharField(max_length=40)),
                ('code', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('type', models.IntegerField(choices=[(0, 'Undefined'), (1, 'Seed'), (2, 'Resource'), (3, 'Kit'), (4, 'fruit')], default='Item.UNDEFINED')),
                ('store_price', models.IntegerField(default=2)),
                ('sold_price', models.IntegerField(default=1)),
                ('display_fields', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('generator', models.CharField(blank=True, max_length=255, null=True)),
                ('rules', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
            ],
        ),
    ]
