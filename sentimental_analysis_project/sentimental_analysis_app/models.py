from django.db import models

# Create your models here.

class Emotions(models.Model):
    x = models.IntegerField()
    emotions = models.CharField(max_length=30, null=True)



class DemonitisationTweets(models.Model):
    x = models.CharField(max_length=30)
    tweet_id = models.CharField(max_length=30,null=True)
    text = models.CharField(max_length=700,null=True)
    favorited = models.CharField(max_length=30,null=True)
    favorite_count = models.IntegerField(null=True) # likes
    reply_to_sn = models.CharField(max_length=30,null=True)
    created = models.CharField(max_length=30,null=True)# TODO use date time with DD-MM-YYYY hh:mm
    truncated = models.CharField(max_length=30,null=True)
    reply_to_sid = models.CharField(max_length=30,null=True)
    reply_to_uid = models.CharField(max_length=30,null=True)
    status_source = models.CharField(max_length=150,null=True)
    screen_name = models.CharField(max_length=30,null=True)
    retweet_count = models.IntegerField(null=True)
    is_retweet = models.CharField(max_length=30,null=True)
    retweeted = models.CharField(max_length=30,null=True)
    # Newly added columns
    sentiment_compound_polarity = models.CharField(max_length=30, null=True) # it should support 4 decimal places
    sentiment_neutral = models.CharField(max_length=30, null=True) # it should support 4 decimal places
    sentiment_negative = models.CharField(max_length=30, null=True) # it should support 4 decimal places
    sentiment_pos = models.CharField(max_length=30, null=True) # it should support 4 decimal places
    sentiment_type = models.CharField(max_length=20, null=True)
    date = models.CharField(max_length=30, null=True)
    hour = models.IntegerField(null=True)
    minute = models.IntegerField(null=True)
    emotions = models.CharField(max_length=30, null=True)
    device_type = models.CharField(max_length=300, null=True)
