# Generated by Django 3.1.4 on 2021-02-15 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gshs', '0020_auto_20210215_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='buseo',
            field=models.SmallIntegerField(choices=[(1, '부서'), (2, '강의실'), (3, '강당'), (4, '실험실'), (5, '기타')], default=1, max_length=2),
        ),
    ]