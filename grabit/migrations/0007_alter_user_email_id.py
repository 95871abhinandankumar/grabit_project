# Generated by Django 4.0.3 on 2022-03-15 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grabit', '0006_alter_user_email_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email_id',
            field=models.EmailField(max_length=254),
        ),
    ]
