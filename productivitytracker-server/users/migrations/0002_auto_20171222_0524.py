# Generated by Django 2.0 on 2017-12-22 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='details',
            name='country',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='details',
            name='goal',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='details',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
