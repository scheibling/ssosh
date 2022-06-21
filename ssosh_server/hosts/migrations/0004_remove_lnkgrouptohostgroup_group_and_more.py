# Generated by Django 4.0.5 on 2022-06-20 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0003_alter_host_grouplink_alter_host_key_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lnkgrouptohostgroup',
            name='group',
        ),
        migrations.RemoveField(
            model_name='lnkgrouptohostgroup',
            name='hostgroup',
        ),
        migrations.RemoveField(
            model_name='lnkhosttohostgroup',
            name='group',
        ),
        migrations.RemoveField(
            model_name='lnkhosttohostgroup',
            name='host',
        ),
        migrations.RemoveField(
            model_name='testitem',
            name='usrlink',
        ),
        migrations.RemoveField(
            model_name='host',
            name='grouplink',
        ),
        migrations.RemoveField(
            model_name='host',
            name='userlink',
        ),
        migrations.AlterField(
            model_name='host',
            name='key',
            field=models.CharField(default='22983e57-1962-48a6-91c3-c5c027cf6164', max_length=100),
        ),
        migrations.DeleteModel(
            name='LnkGroupToHost',
        ),
        migrations.DeleteModel(
            name='LnkGroupToHostgroup',
        ),
        migrations.DeleteModel(
            name='LnkHostToHostgroup',
        ),
        migrations.DeleteModel(
            name='TestItem',
        ),
        migrations.DeleteModel(
            name='TestUser',
        ),
    ]
