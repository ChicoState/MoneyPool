# Generated by Django 3.1.1 on 2020-09-25 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=20)),
                ('lastName', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
            ],
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]