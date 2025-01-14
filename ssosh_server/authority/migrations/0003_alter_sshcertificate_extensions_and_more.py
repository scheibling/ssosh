# Generated by Django 4.0.5 on 2022-06-23 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authority', '0002_alter_sshcertificate_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sshcertificate',
            name='extensions',
            field=models.TextField(default='permit-agent-forwarding,permit-X11-forwarding', null=True),
        ),
        migrations.AlterField(
            model_name='sshcertificate',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
