# Generated by Django 5.0.6 on 2024-05-15 00:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0003_memberprofile_college_memberprofile_interest_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='memberprofile',
            old_name='college',
            new_name='course',
        ),
    ]
