# Generated by Django 4.1.7 on 2023-02-23 10:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentsuser',
            name='password',
        ),
    ]