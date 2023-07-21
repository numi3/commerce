# Generated by Django 4.1.6 on 2023-07-06 08:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_auction_current_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='current_bid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='auction_bids', to='auctions.bid'),
        ),
    ]