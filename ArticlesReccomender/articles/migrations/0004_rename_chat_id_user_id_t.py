# Generated by Django 4.1.5 on 2023-02-13 18:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_user_like'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='chat_id',
            new_name='id_t',
        ),
    ]