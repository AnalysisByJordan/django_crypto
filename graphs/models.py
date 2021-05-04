from django.db import models

# Create your models here.
class cryptoData(models.Model):
    coin = models.CharField(max_length=10)
    asset_id = models.SmallIntegerField()
    time = models.DateTimeField()
    close = models.FloatField()
    volume = models.BigIntegerField()
    market_cap = models.FloatField()
    reddit_posts = models.IntegerField()
    reddit_comments = models.IntegerField()
    tweets = models.IntegerField()
    tweet_favorites = models.IntegerField()
    social_volume = models.IntegerField()