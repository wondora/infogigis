# Generated by Django 3.1.4 on 2021-01-21 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gshs', '0006_auto_20210121_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gigirental',
            name='due_date',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]
