# Generated by Django 4.1.3 on 2023-06-06 05:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calc_app', '0003_admixture_alter_contractequipment_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fullwaterparametrs',
            name='exceeding_consequence',
        ),
        migrations.RemoveField(
            model_name='fullwaterparametrs',
            name='recommendations',
        ),
    ]