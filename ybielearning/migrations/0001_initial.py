# Generated by Django 3.0.8 on 2020-08-17 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.CharField(max_length=120)),
                ('username', models.CharField(blank=True, max_length=120, null=True)),
                ('firstname', models.CharField(blank=True, max_length=120, null=True)),
                ('lastname', models.CharField(blank=True, max_length=120, null=True)),
                ('fullname', models.CharField(blank=True, max_length=120, null=True)),
                ('email', models.CharField(blank=True, max_length=120, null=True)),
                ('idnumber', models.CharField(blank=True, max_length=120, null=True)),
                ('suspended', models.CharField(blank=True, max_length=120, null=True)),
            ],
        ),
    ]