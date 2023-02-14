# Generated by Django 4.1.5 on 2023-01-14 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doi', models.CharField(max_length=100)),
                ('keywords', models.TextField(default='')),
                ('url', models.CharField(max_length=1000)),
            ],
        ),
    ]