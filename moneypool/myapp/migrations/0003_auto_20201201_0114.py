# Generated by Django 3.1.1 on 2020-12-01 01:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20201130_2153'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='question',
            name='pub_date',
        ),
    ]
