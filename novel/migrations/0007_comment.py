# Generated by Django 4.0.2 on 2022-04-30 15:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('novel', '0006_userbookshelfbook_delete_userbookshelf'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('active', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('novel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='novel.novel')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='novel.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created_on'],
            },
        ),
    ]