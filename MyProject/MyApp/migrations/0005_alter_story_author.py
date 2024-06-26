# Generated by Django 4.2.11 on 2024-03-22 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("MyApp", "0004_alter_story_author"),
    ]

    operations = [
        migrations.AlterField(
            model_name="story",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="MyApp.author"
            ),
        ),
    ]
