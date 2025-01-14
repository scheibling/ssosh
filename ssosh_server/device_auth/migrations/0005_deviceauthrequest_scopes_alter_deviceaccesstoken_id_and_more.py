# Generated by Django 4.0.5 on 2022-06-22 13:35

from django.db import migrations, models
import ssosh_server.device_auth.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('device_auth', '0004_alter_deviceaccesstoken_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='deviceauthrequest',
            name='scopes',
            field=models.CharField(default='client.bootstrap', max_length=255),
        ),
        migrations.AlterField(
            model_name='deviceaccesstoken',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='deviceaccesstoken',
            name='token',
            field=models.CharField(default=ssosh_server.device_auth.models.token_32bit, max_length=120, unique=True),
        ),
        migrations.AlterField(
            model_name='deviceauthrequest',
            name='code',
            field=models.CharField(default=ssosh_server.device_auth.models.token_32bit, max_length=120, unique=True),
        ),
        migrations.AlterField(
            model_name='deviceauthrequest',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
