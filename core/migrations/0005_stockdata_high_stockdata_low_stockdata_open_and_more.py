# Generated by Django 4.2.2 on 2023-06-29 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_tickerlist_stockinfo_symbol_stockinfo_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockdata',
            name='High',
            field=models.FloatField(default=25.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stockdata',
            name='Low',
            field=models.FloatField(default=25.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stockdata',
            name='Open',
            field=models.FloatField(default=12.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stockdata',
            name='Volume',
            field=models.FloatField(default=25.0),
            preserve_default=False,
        ),
    ]