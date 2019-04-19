# Generated by Django 2.2 on 2019-04-18 06:27

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='installments_payed',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.jsonb.JSONField(), default=list, size=None, verbose_name='History of installments payed'),
        ),
        migrations.AddField(
            model_name='mobile',
            name='is_sold',
            field=models.BooleanField(default=False, verbose_name='Is product sold'),
        ),
        migrations.AddField(
            model_name='transactions',
            name='amount_remaining',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='transactions',
            name='is_return',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_customer', to='accounts.User'),
        ),
        migrations.AlterField(
            model_name='user',
            name='CNIC_number',
            field=models.CharField(max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='father_name',
            field=models.CharField(blank=True, max_length=60),
        ),
    ]
