# Generated by Django 2.2 on 2019-04-25 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_remove_mobile_brand'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mobile',
            name='mobile_status',
        ),
    ]
