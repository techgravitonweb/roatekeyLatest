# Generated by Django 4.0.3 on 2022-09-02 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_reviewsection_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.CharField(default='null', max_length=150),
        ),
    ]