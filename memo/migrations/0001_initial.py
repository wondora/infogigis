# Generated by Django 3.1.4 on 2021-02-04 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Memo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
            ],
            options={
                'db_table': 'memo',
                'ordering': ['-created_date'],
            },
        ),
    ]
