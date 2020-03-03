# Generated by Django 2.2.1 on 2019-06-05 21:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_machineservice_registerphoto'),
    ]

    operations = [
        migrations.CreateModel(
            name='PermittedMachine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_permitted', models.IntegerField()),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='machine_permitterd', to='service.MachineService')),
            ],
            options={
                'verbose_name_plural': 'Register Photo Models',
            },
        ),
    ]