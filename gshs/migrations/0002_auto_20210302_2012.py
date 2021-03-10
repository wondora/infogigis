# Generated by Django 3.1.4 on 2021-03-02 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gshs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='people',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='주소'),
        ),
        migrations.AlterField(
            model_name='people',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='성명'),
        ),
    ]