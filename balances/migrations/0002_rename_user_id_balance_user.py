# Generated by Django 4.1.7 on 2023-02-26 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('balances', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='balance',
            old_name='user_id',
            new_name='user',
        ),
    ]