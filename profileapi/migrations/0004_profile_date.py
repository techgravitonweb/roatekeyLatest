# Generated by Django 4.0.3 on 2022-12-23 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profileapi', '0003_alter_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='date',
            field=models.CharField(default='2022-12-23', max_length=10),
        ),
    ]