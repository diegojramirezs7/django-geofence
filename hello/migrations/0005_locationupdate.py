# Generated by Django 3.1.6 on 2021-02-02 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0004_auto_20210115_0016'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationUpdate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('time', models.DateTimeField(verbose_name='recorded')),
            ],
        ),
    ]
