# Generated by Django 3.0.8 on 2020-10-08 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docmgt', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='lastupdatetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='lastupdateuser',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]