# Generated by Django 3.1.4 on 2021-01-21 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gshs', '0003_gigirental'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gigirental',
            name='jaego',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gshs.jaego'),
        ),
    ]
