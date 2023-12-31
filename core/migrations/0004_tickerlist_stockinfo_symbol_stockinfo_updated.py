# Generated by Django 4.2.2 on 2023-06-28 22:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_stockinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='TickerList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Symbol', models.CharField(max_length=50)),
                ('Name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='stockinfo',
            name='Symbol',
            field=models.CharField(default=datetime.datetime(2023, 6, 28, 22, 52, 36, 925988, tzinfo=datetime.timezone.utc), max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stockinfo',
            name='Updated',
            field=models.DateField(default=datetime.datetime(2023, 6, 28, 22, 53, 27, 48414, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]
