# Generated by Django 3.2.8 on 2021-11-15 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tutorial', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='cover_img',
        ),
        migrations.AddField(
            model_name='post',
            name='cover_img_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]