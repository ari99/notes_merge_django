# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-04 21:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_chars', models.IntegerField()),
                ('num_lines', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UsageSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(max_length=1200)),
            ],
        ),
        migrations.AddField(
            model_name='usage',
            name='usage_session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notesmerge.UsageSession'),
        ),
    ]
