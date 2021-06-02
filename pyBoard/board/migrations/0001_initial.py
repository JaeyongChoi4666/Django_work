# Generated by Django 3.2.3 on 2021-06-02 06:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('idx', models.AutoField(primary_key=True, serialize=False)),
                ('writer', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('hit', models.IntegerField(default=0)),
                ('post_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('filename', models.CharField(blank=True, default='', max_length=500, null=True)),
                ('filesize', models.IntegerField(default=0)),
                ('cnt_download', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('idx', models.AutoField(primary_key=True, serialize=False)),
                ('board_idx', models.IntegerField()),
                ('writer', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('post_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
    ]
