# Generated by Django 4.0 on 2022-02-04 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('host', '0003_remove_host_group_permission_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='key',
            field=models.CharField(default='9f4ea698-3651-4720-959b-2070313c80da', max_length=100),
        ),
    ]
