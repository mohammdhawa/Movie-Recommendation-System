# Generated by Django 4.2.13 on 2024-06-02 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_profile_get_user_id_from_dataset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='users/user.png', null=True, upload_to='users'),
        ),
    ]
