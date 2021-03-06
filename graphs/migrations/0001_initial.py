# Generated by Django 3.2 on 2021-04-15 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='cryptoData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin', models.CharField(max_length=10)),
                ('asset_id', models.SmallIntegerField()),
                ('time', models.DateTimeField()),
                ('close', models.FloatField()),
                ('volume', models.BigIntegerField()),
                ('market_cap', models.FloatField()),
                ('reddit_posts', models.IntegerField()),
                ('reddit_comments', models.IntegerField()),
                ('tweets', models.IntegerField()),
                ('tweet_favorites', models.IntegerField()),
                ('social_volume', models.IntegerField()),
            ],
        ),
    ]
