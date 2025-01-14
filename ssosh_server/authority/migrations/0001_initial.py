# Generated by Django 4.0.5 on 2022-06-23 13:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import ssosh_server.authority.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client', '0002_alter_device_active_alter_device_hostname_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SSHCertificate',
            fields=[
                ('id', models.PositiveBigIntegerField(primary_key=True, serialize=False)),
                ('key_id', models.TextField(unique=True)),
                ('public_key', models.TextField()),
                ('cert_type', models.IntegerField(choices=[(1, 'User'), (2, 'Host')])),
                ('principals', models.TextField()),
                ('valid_after', models.DateTimeField(default=django.utils.timezone.now)),
                ('valid_before', models.DateTimeField(default=ssosh_server.authority.models.get_default_validity)),
                ('critical', models.TextField(blank=True, default='', null=True)),
                ('extensions', models.TextField(blank=True, default='permit-agent-forwarding,permit-X11-forwarding', null=True)),
                ('signature', models.TextField()),
                ('requested_at', models.DateTimeField(auto_now_add=True)),
                ('signed', models.BooleanField(default=False)),
                ('requested_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('requested_from', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='client.device')),
            ],
        ),
    ]
