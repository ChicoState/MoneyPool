# Generated by Django 3.1.1 on 2020-12-01 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_question_end_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
