# Generated by Django 4.0.5 on 2022-06-21 13:27

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('device_auth', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deviceaccesstoken',
            name='device',
        ),
        migrations.AlterField(
            model_name='deviceaccesstoken',
            name='id',
            field=models.UUIDField(default=uuid.UUID('7c1cf2f3-69f9-4a35-921d-4de3cd050dd1'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='deviceaccesstoken',
            name='time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='deviceaccesstoken',
            name='token',
            field=models.CharField(default='fn_9LSAI3R1STrUOp05F_bb9xA068JIsGXQye1loxIE', max_length=120, unique=True),
        ),
        migrations.AlterField(
            model_name='deviceauthrequest',
            name='code',
            field=models.CharField(default='Wvg-JC77rFituRCpQT0w4w', max_length=120, unique=True),
        ),
        migrations.AlterField(
            model_name='deviceauthrequest',
            name='id',
            field=models.UUIDField(default=uuid.UUID('4ce71df9-fa6a-41b9-93eb-6fe8296339e3'), editable=False, primary_key=True, serialize=False),
        ),
    ]
