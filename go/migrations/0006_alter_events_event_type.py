# Generated by Django 3.2.9 on 2021-12-02 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('go', '0005_auto_20211202_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='event_type',
            field=models.CharField(help_text='event type', max_length=500, null=True, verbose_name='type'),
        ),
    ]
