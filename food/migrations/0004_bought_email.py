# Generated by Django 5.0.1 on 2024-08-17 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0003_bought_boughtitems'),
    ]

    operations = [
        migrations.AddField(
            model_name='bought',
            name='email',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
