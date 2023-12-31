# Generated by Django 4.2.2 on 2023-07-03 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_stockdata_residue_stockdata_seasonal_stockdata_trend'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockdata',
            name='BollBottom',
            field=models.FloatField(default=25.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stockdata',
            name='BollTop',
            field=models.FloatField(default=25.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stockdata',
            name='MovAvg',
            field=models.FloatField(default=25.0),
            preserve_default=False,
        ),
    ]
