# Generated by Django 4.0.5 on 2022-06-20 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0013_alter_host_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostgroup',
            name='hostlink',
            field=models.ManyToManyField(blank=True, related_name='host_link', to='hosts.host', verbose_name='Hosts'),
        ),
        migrations.AlterField(
            model_name='host',
            name='key',
            field=models.CharField(default='326c77ec-cbfe-45ee-ad10-c8b2e7846814', max_length=100),
        ),
    ]
