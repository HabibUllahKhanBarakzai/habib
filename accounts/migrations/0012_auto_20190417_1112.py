# Generated by Django 2.2 on 2019-04-17 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20190417_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='CNIC_number',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]