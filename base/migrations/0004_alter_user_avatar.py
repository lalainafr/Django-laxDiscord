# Generated by Django 5.0.1 on 2024-02-12 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='profile.png', null=True, upload_to=''),
        ),
    ]
