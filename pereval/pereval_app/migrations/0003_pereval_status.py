# Generated by Django 5.0.4 on 2024-04-30 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pereval_app', '0002_images_delete_image_remove_level_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pereval',
            name='status',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
    ]
