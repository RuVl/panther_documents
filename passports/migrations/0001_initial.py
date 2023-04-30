# Generated by Django 4.1.7 on 2023-04-30 09:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='Passport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('count', models.IntegerField()),
                ('ruble_cost', models.FloatField()),
                ('dollar_cost', models.FloatField()),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='passports.country')),
            ],
            options={
                'verbose_name': 'Passport',
                'verbose_name_plural': 'Passports',
            },
        ),
    ]
