# Generated by Django 3.0.8 on 2020-09-18 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it', '0004_auto_20200918_0837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffbirthday',
            name='birthdaydate',
            field=models.DateTimeField(),
        ),
    ]
