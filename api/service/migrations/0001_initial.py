# Generated by Django 2.2.1 on 2019-05-30 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceModels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.CharField(max_length=125)),
                ('machine', models.CharField(max_length=125)),
                ('project', models.CharField(max_length=125)),
                ('zone', models.CharField(max_length=50)),
                ('instance', models.CharField(max_length=125)),
                ('status', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Service Models',
            },
        ),
    ]
