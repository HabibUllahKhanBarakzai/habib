# Generated by Django 2.2 on 2019-05-06 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supply', '0007_auto_20190430_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='next_installment_due',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='received_at',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='purchase_date',
            field=models.DateField(),
        ),
    ]