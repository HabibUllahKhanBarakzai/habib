# Generated by Django 2.2 on 2019-04-27 23:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supply', '0002_auto_20190426_0649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='next_installment_due',
            field=models.DateField(default=datetime.date(2019, 5, 27)),
        ),
        migrations.AlterField(
            model_name='order',
            name='received_at',
            field=models.DateField(default=datetime.date(2019, 4, 27)),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='purchase_date',
            field=models.DateField(default=datetime.date(2019, 4, 27)),
        ),
    ]
