# Generated by Django 3.0.8 on 2020-09-09 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbielearning', '0002_user_priority'),
    ]

    operations = [
        migrations.CreateModel(
            name='BBBbn_logs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseid', models.CharField(blank=True, max_length=120, null=True)),
                ('userid', models.CharField(blank=True, max_length=120, null=True)),
                ('timecreated', models.CharField(blank=True, max_length=120, null=True)),
                ('meetingid', models.CharField(blank=True, max_length=120, null=True)),
                ('log', models.CharField(blank=True, max_length=120, null=True)),
                ('meta', models.CharField(blank=True, max_length=120, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BBBRecordings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recordid', models.CharField(blank=True, max_length=120, null=True)),
                ('meetingid', models.CharField(blank=True, max_length=120, null=True)),
                ('name', models.CharField(blank=True, max_length=120, null=True)),
                ('published', models.CharField(blank=True, max_length=120, null=True)),
                ('state', models.CharField(blank=True, max_length=120, null=True)),
                ('starttime', models.CharField(blank=True, max_length=120, null=True)),
                ('endtime', models.CharField(blank=True, max_length=120, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='priority',
            field=models.CharField(blank=True, choices=[('priority', 'Priority'), ('normal', 'Normal'), ('', '')], max_length=120, null=True),
        ),
    ]
