# Generated by Django 4.0.5 on 2022-06-20 13:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hosts', '0007_alter_host_grouplink_alter_host_hostgrouplink_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hostgroup',
            options={'verbose_name': 'Hostgroup', 'verbose_name_plural': 'Hostgroups'},
        ),
        migrations.AddField(
            model_name='hostgroup',
            name='hostlink',
            field=models.ManyToManyField(blank=True, related_name='hostgroup_link', to='hosts.host', verbose_name='Hosts'),
        ),
        migrations.AlterField(
            model_name='host',
            name='grouplink',
            field=models.ManyToManyField(blank=True, related_name='group_link', to='auth.group', verbose_name='Groups'),
        ),
        migrations.AlterField(
            model_name='host',
            name='hostgrouplink',
            field=models.ManyToManyField(blank=True, related_name='hostgroup_link', to='hosts.hostgroup', verbose_name='Hostgroups'),
        ),
        migrations.AlterField(
            model_name='host',
            name='key',
            field=models.CharField(default='1474498c-10ab-4aab-a0a8-be7140211d0d', max_length=100),
        ),
        migrations.AlterField(
            model_name='host',
            name='userlink',
            field=models.ManyToManyField(blank=True, related_name='user_link', to=settings.AUTH_USER_MODEL, verbose_name='Users'),
        ),
        migrations.AlterField(
            model_name='hostgroup',
            name='slug',
            field=models.SlugField(max_length=128, unique=True, verbose_name='Slug (a-zA-Z0-9\\-\\_)'),
        ),
    ]