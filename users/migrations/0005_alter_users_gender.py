# Generated by Django 4.1.3 on 2022-11-11 19:15

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_users_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='gender',
            field=models.ForeignKey(default=(), null=True, on_delete=users.models.gender_default, to='users.gender_of_user'),
        ),
    ]
