# Generated by Django 3.2.12 on 2022-04-05 17:12

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20220327_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 7, 17, 12, 56, 238457, tzinfo=utc)),
        ),
    ]
