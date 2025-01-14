# Generated by Django 4.0.5 on 2022-06-20 13:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hosts', '0005_host_userlink_alter_host_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='grouplink',
            field=models.ManyToManyField(related_name='group_link', to=settings.AUTH_USER_MODEL, verbose_name='Group permissions'),
        ),
        migrations.AddField(
            model_name='host',
            name='hostgrouplink',
            field=models.ManyToManyField(related_name='hostgroup_link', to=settings.AUTH_USER_MODEL, verbose_name='Hostgroup Permissions'),
        ),
        migrations.AlterField(
            model_name='host',
            name='key',
            field=models.CharField(default='6c32d113-d6e0-4d47-bb35-3487865d9088', max_length=100),
        ),
        migrations.AlterField(
            model_name='host',
            name='userlink',
            field=models.ManyToManyField(related_name='user_link', to=settings.AUTH_USER_MODEL, verbose_name='User permissions'),
        ),
    ]
