# Generated by Django 4.0.5 on 2022-06-20 14:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hosts', '0014_hostgroup_hostlink_alter_host_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostgroup',
            name='grouplink',
            field=models.ManyToManyField(blank=True, related_name='hostgroup_group_link', to='auth.group', verbose_name='Groups'),
        ),
        migrations.AddField(
            model_name='hostgroup',
            name='userlink',
            field=models.ManyToManyField(blank=True, related_name='hostgroup_user_link', to=settings.AUTH_USER_MODEL, verbose_name='Users'),
        ),
        migrations.AlterField(
            model_name='host',
            name='grouplink',
            field=models.ManyToManyField(blank=True, related_name='host_group_link', to='auth.group', verbose_name='Groups'),
        ),
        migrations.AlterField(
            model_name='host',
            name='hostgrouplink',
            field=models.ManyToManyField(blank=True, related_name='host_hostgroup_link', to='hosts.hostgroup', verbose_name='Hostgroups'),
        ),
        migrations.AlterField(
            model_name='host',
            name='key',
            field=models.CharField(default='057efdcd-9088-44e9-90d3-a9b2af4ed0cd', max_length=100),
        ),
        migrations.AlterField(
            model_name='host',
            name='userlink',
            field=models.ManyToManyField(blank=True, related_name='host_user_link', to=settings.AUTH_USER_MODEL, verbose_name='Users'),
        ),
        migrations.AlterField(
            model_name='hostgroup',
            name='hostlink',
            field=models.ManyToManyField(blank=True, related_name='hostgroup_host_link', to='hosts.host', verbose_name='Hosts'),
        ),
    ]