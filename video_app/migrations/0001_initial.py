# Generated by Django 3.2.5 on 2021-07-05 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='api_keys',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_key', models.CharField(max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='videos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, null=True)),
                ('description', models.CharField(max_length=2000, null=True)),
                ('date', models.DateField(null=True)),
                ('photo', models.DateField(null=True)),
                ('url', models.DateField(null=True)),
            ],
        ),
    ]
