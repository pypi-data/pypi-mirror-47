# Generated by Django 2.2.1 on 2019-05-07 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issuestracker', '0009_auto_20190501_1852'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='date_added',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
