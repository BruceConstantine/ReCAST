# Generated by Django 3.0.6 on 2020-05-13 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ReCAST', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='cid',
            field=models.IntegerField(null=True),
        ),
    ]
