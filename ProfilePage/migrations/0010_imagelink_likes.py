# Generated by Django 3.1 on 2020-03-24 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProfilePage', '0009_account_purchased'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagelink',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
