# Generated by Django 4.0.5 on 2022-06-21 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0016_alter_host_options_alter_host_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='key',
            field=models.CharField(default='accd98a1-6110-4a59-b00b-b53f32d1de5e', max_length=100),
        ),
    ]
