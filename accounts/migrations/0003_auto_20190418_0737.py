# Generated by Django 2.2 on 2019-04-18 07:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20190418_0627'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='Our_User',
        ),
    ]