# Generated by Django 2.2 on 2019-04-25 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supply', '0002_auto_20190425_1225'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='amount_remaining',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
