# Generated by Django 3.1.4 on 2021-02-15 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gshs', '0019_productgubun_table_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='buseo',
            field=models.SmallIntegerField(default=1, max_length=2),
        ),
    ]