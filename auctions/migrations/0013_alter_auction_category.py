# Generated by Django 4.2 on 2023-09-10 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_rename_created_at_comment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='category',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
