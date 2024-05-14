# Generated by Django 5.0.6 on 2024-05-14 17:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='announcements',
            field=models.ManyToManyField(blank=True, null=True, related_name='announcements', to='clubs.announcement'),
        ),
        migrations.AlterField(
            model_name='club',
            name='discussions',
            field=models.ManyToManyField(blank=True, null=True, related_name='discussions', to='clubs.discussion'),
        ),
        migrations.AlterField(
            model_name='club',
            name='events',
            field=models.ManyToManyField(blank=True, null=True, related_name='events', to='clubs.event'),
        ),
        migrations.AlterField(
            model_name='club',
            name='members',
            field=models.ManyToManyField(blank=True, null=True, related_name='clubmembers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='discussion',
            name='members',
            field=models.ManyToManyField(blank=True, null=True, related_name='members', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='event',
            name='attendees',
            field=models.ManyToManyField(blank=True, null=True, related_name='attendees', to=settings.AUTH_USER_MODEL),
        ),
    ]