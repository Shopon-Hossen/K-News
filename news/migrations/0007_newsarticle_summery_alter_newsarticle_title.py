# Generated by Django 5.1.2 on 2024-10-30 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_newsarticle_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsarticle',
            name='summery',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='newsarticle',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
