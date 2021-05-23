# Generated by Django 3.2.2 on 2021-05-13 15:30

from django.db import migrations, models
import mainapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_auto_20210513_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='code',
            field=models.CharField(default=mainapp.models.make_code, max_length=9, unique=True),
        ),
    ]