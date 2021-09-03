# Generated by Django 3.2.6 on 2021-09-01 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurance_app', '0003_customer_customer_digit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_income_group',
            field=models.IntegerField(choices=[(0, '0- $25K'), (1, '$25-$70K'), (2, '>$70K')], default=0),
        ),
        migrations.AlterField(
            model_name='policydetails',
            name='fuel',
            field=models.IntegerField(choices=[(0, 'CNG'), (1, 'Petrol'), (2, 'Diesel')]),
        ),
    ]
