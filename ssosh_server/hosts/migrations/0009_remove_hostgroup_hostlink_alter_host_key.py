# Generated by Django 4.0.5 on 2022-06-20 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0008_alter_hostgroup_options_hostgroup_hostlink_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hostgroup',
            name='hostlink',
        ),
        migrations.AlterField(
            model_name='host',
            name='key',
            field=models.CharField(default='c8909e91-08ed-4cef-8ea1-95b90604746b', max_length=100),
        ),
    ]
