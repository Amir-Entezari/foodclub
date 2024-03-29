# Generated by Django 4.1.3 on 2022-11-23 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0011_alter_customer_options_remove_customer_email_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'permissions': [('cancel_order', 'Can cancel order')]},
        ),
        migrations.AlterField(
            model_name='customer',
            name='birth_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
