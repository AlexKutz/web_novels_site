# Generated by Django 4.0.2 on 2022-03-08 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novel', '0006_alter_novel_book_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='novel',
            name='book_image',
            field=models.ImageField(upload_to='./novel/book_cover'),
        ),
    ]
