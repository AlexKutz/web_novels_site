# Generated by Django 4.0.2 on 2022-03-23 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='number',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
