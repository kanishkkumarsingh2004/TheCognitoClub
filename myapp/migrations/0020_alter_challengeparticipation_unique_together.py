# Generated by Django 5.1.6 on 2025-03-03 12:04

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0019_alter_challengeparticipation_unique_together'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='challengeparticipation',
            unique_together={('user', 'challenge')},
        ),
    ]
