# Generated by Django 4.1.3 on 2022-11-22 07:41

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0006_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]
