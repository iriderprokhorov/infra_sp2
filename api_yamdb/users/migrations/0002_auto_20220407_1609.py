# Generated by Django 2.2.16 on 2022-04-07 16:09

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.UUIDField(default=uuid.UUID('e1b36f9a-b496-4e21-8e19-6e067628e1d8'), verbose_name='UUID'),
        ),
    ]
