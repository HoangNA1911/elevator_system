# Generated by Django 4.2.3 on 2024-11-09 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Elevator',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('current_floor', models.IntegerField(default=1)),
                ('status', models.CharField(choices=[('up', 'Up'), ('down', 'Down'), ('idle', 'Idle')], default='idle', max_length=4)),
                ('target_floors', models.JSONField(default=list)),
                ('is_open', models.BooleanField(default=False)),
            ],
        ),
    ]
