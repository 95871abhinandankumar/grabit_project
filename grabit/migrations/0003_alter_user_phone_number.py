# Generated by Django 4.0.3 on 2022-03-14 18:11

import django.core.validators
from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('grabit', '0002_rename_users_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None, validators=[django.core.validators.RegexValidator('^\\d{3}-\\d{3}-\\d{4}$')]),
        ),
    ]