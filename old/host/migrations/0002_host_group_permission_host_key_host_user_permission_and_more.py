# Generated by Django 4.0 on 2022-02-04 15:00

from django.conf import settings
from django.db import migrations, models
import ssosh_server.host.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('host', '0001_initial'),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='host',
        #     name='group_permission',
        #     field=models.ManyToManyField(to='auth.Group'),
        # ),
        # migrations.AddField(
        #     model_name='host',
        #     name='key',
        #     field=models.CharField(default=' ', max_length=100),
        #     preserve_default=False,
        # ),
        # migrations.AddField(
        #     model_name='host',
        #     name='user_permission',
        #     field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='user list'),
        # ),
        migrations.AlterField(
            model_name='host',
            name='hostname',
            field=ssosh_server.host.models.UpperCaseCharField(max_length=255),
        ),
    ]
