# Generated by Django 5.1.2 on 2024-10-29 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_newsarticle_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.CharField(max_length=200),
        ),
    ]