# Generated by Django 4.0.3 on 2022-03-15 10:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grabit', '0005_alter_user_email_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email_id',
            field=models.EmailField(max_length=254, validators=[django.core.validators.RegexValidator('^[a-z][a-z0-9]+@iiitg.ac.in$', message='Institute email-id required to register')]),
        ),
    ]