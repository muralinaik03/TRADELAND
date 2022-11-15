# Generated by Django 4.1.3 on 2022-11-15 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0009_alter_property_details_map_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='featured',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('text', models.CharField(max_length=30)),
                ('city_state', models.CharField(max_length=25)),
                ('pincode', models.CharField(max_length=6)),
                ('prop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.property')),
            ],
        ),
    ]
