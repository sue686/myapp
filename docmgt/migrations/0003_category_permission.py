# Generated by Django 3.0.8 on 2020-11-25 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docmgt', '0002_auto_20201008_1408'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='permission',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
