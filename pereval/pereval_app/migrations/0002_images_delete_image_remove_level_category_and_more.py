# Generated by Django 5.0.4 on 2024-04-28 19:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pereval_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.ImageField(upload_to='')),
                ('title', models.CharField(max_length=100)),
                ('pereval', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pereval_app.pereval')),
            ],
        ),
        migrations.DeleteModel(
            name='Image',
        ),
        migrations.RemoveField(
            model_name='level',
            name='category',
        ),
        migrations.RemoveField(
            model_name='level',
            name='difficulty_level',
        ),
        migrations.AddField(
            model_name='level',
            name='autumn',
            field=models.CharField(default=1, max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='level',
            name='spring',
            field=models.CharField(default=1, max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='level',
            name='summer',
            field=models.CharField(default=1, max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='level',
            name='winter',
            field=models.CharField(default=1, max_length=2),
            preserve_default=False,
        ),
    ]
