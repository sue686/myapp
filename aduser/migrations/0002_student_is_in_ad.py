# Generated by Django 4.0.5 on 2024-07-21 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aduser', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='is_in_AD',
            field=models.CharField(default='n', help_text='y means yes, n means no', max_length=1),
        ),
    ]
