# Generated by Django 5.1.6 on 2025-03-01 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_challenge'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='usn',
            field=models.CharField(default=1234567890, max_length=20, unique=True),
            preserve_default=False,
        ),
    ]
