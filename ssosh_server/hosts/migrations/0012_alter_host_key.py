# Generated by Django 4.0.5 on 2022-06-20 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0011_alter_host_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='key',
            field=models.CharField(default='63c06724-c1f8-47c4-b225-4c13b0f7fb72', max_length=100),
        ),
    ]