# Generated by Django 3.0.8 on 2020-07-23 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20200723_1612'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='imageFilelocation',
        ),
        migrations.AddField(
            model_name='user',
            name='imageFile',
            field=models.FileField(blank=True, null=True, upload_to='media/', verbose_name=''),
        ),
    ]
