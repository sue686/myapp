# Generated by Django 3.0.8 on 2020-11-15 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ybielearning', '0010_userbulk'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='priority',
            field=models.CharField(blank=True, choices=[('priority', 'Priority'), ('normal', 'Normal'), ('', '')], max_length=120, null=True),
        ),
    ]
