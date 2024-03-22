# Generated by Django 4.2.11 on 2024-03-22 11:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("MyApp", "0003_alter_story_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="story",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
