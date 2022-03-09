# Generated by Django 4.0.2 on 2022-03-08 17:00

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('novel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
                ('abbreviation', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Novel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, unique=True)),
                ('alt_title', models.CharField(blank=True, max_length=64, verbose_name='alternative title')),
                ('adult_only', models.BooleanField(default=False)),
                ('words', models.PositiveIntegerField(verbose_name='number of words')),
                ('createrd_at', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='novel.author')),
                ('language', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='novel.language')),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)])),
                ('novel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='novel.novel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='novel',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='novel.status'),
        ),
        migrations.AddField(
            model_name='novel',
            name='tags',
            field=models.ManyToManyField(to='novel.Tag'),
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=16)),
                ('content', models.TextField()),
                ('createrd_at', models.DateTimeField(auto_now_add=True)),
                ('novel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='novel.novel')),
            ],
        ),
    ]
