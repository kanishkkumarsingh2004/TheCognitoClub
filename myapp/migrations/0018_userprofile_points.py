# Generated by Django 5.1.6 on 2025-03-02 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0017_challengeparticipation_review_notes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='points',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
