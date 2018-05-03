from sentimental_analysis_app.models import DemonitisationTweets
from sentimental_analysis_app.utils.analysis import get_analized_sentiments,\
get_emotion_to_x_map,get_tweets_device_dict
from sentimental_analysis_app.utils.data_reader import check_emotions_in_db, get_emotions_to_x_map_from_db
import os
import csv
from datetime import datetime
from django.db import connection
from contextlib import closing
from django.db import connection
from django.utils import timezone
import datetime



def write_emotions_to_db(emotion_map):
    connection.close()
    sql = 'INSERT INTO sentimental_analysis_app_emotions (x,emotions) VALUES {}'

    params = []

    for key, val in emotion_map.items():
        try:
            values = '({x},"{emotions}")'.format(x=key, emotions=val)
            params.append(values)
        except Exception as err:
            pass
    with closing(connection.cursor()) as cursor:
        values_section = ",".join(params)
        sql = sql.format(values_section)
        cursor.execute(sql)


def set_analyzed_sentiment_to_data_set(data_set):
    analyzed_data = get_analized_sentiments()
    # Check if tweets are already processed for emotions.
    if check_emotions_in_db():
        print ("Getting the emotions from DB...")
        emotion_map = get_emotions_to_x_map_from_db()
    else:
        print ("Getting it from emotions API")
        emotion_map = get_emotion_to_x_map()
        write_emotions_to_db(emotion_map)
    device_type_map = get_tweets_device_dict()
    for ds in data_set:
        # Set sentiment type to dataset
        if int(ds['X']) in analyzed_data['sentiment_type']:
            ds['sentiment_type'] = analyzed_data['sentiment_type'].get(int(ds['X']))
        # Set sentiment emotion to dataset
        if int(ds['X']) in emotion_map:
            ds['emotions'] = emotion_map.get(int(ds['X']))
        # Set sentiment of device type to dataset
        if int(ds['X']) in device_type_map:
            ds['device_type'] = device_type_map.get(int(ds['X']))
        # Split date into hour and minutes.
        f = "%d/%m/%y %H:%M"
        d = datetime.datetime.strptime(ds['created'], f)
        ds['hour'] = d.hour
        ds['minute'] = d.minute


    return data_set


def clean_existing_table_data():
     sql = "DELETE FROM sentimental_analysis_app_demonitisationtweets;"
     with closing(connection.cursor()) as cursor:
        cursor.execute(sql)

def sql_batch_insert(data_set):
    connection.close()
    sql = 'INSERT INTO sentimental_analysis_app_demonitisationtweets (x,tweet_id,text,favorited,favorite_count,reply_to_sn,created,truncated,reply_to_sid,reply_to_uid,status_source,screen_name,retweet_count,is_retweet,retweeted,sentiment_type,emotions,device_type,hour,minute) VALUES {}'

    params = []
   
    for tweet in data_set:
        try:
            values = '({X},{id},"{text}",{favorited},{favorite_count},"{reply_to_sn}","{created}",{truncated},"{reply_to_sid}","{reply_to_uid}","{status_source}","{screen_name}","{retweet_count}",{is_retweet},{retweeted},"{sentiment_type}","{emotions}","{device_type}",{hour},{minute})'.format(X=tweet['X'], id=tweet['id'],
        	                                              text=tweet['text'].replace('"',"'"),favorited=tweet['favorited'],
        	                                              favorite_count=tweet['favoriteCount'],
        												  reply_to_sn=tweet['replyToSN'],
        												  created=tweet['created'],
        												  truncated=tweet['truncated'],
        												  reply_to_sid=tweet['replyToSID'],
        												  reply_to_uid=tweet['replyToUID'],
        												  status_source=tweet['statusSource'].replace('"',"'"),
        												  screen_name=tweet['screenName'].replace('"',"'"),
        												  retweet_count=tweet['retweetCount'],
        												  is_retweet=tweet['isRetweet'],
        												  retweeted=tweet['retweeted'],
        												  sentiment_type = tweet['sentiment_type'],
                                                          emotions = tweet.get('emotions',"NULL"),
                                                          device_type = tweet['device_type'],
                                                          hour = tweet['hour'],
                                                          minute = tweet['minute']
        												  ) 
            params.append(values)
        except Exception as err:
            pass
    with closing(connection.cursor()) as cursor:
        values_section = ",".join(params)
        sql = sql.format(values_section)
        cursor.execute(sql)



# def convert_date_to_django_format(date_str):
#     format = '%d/%m/%y %H:%M'
#     d = datetime.strptime(date_str, format)
#     formated_date = d.strftime("%Y-%m-%d %H:%M:%S")
#     return formated_date

def dump_csv_data_to_db():
    """
    """
    file_path = os.path.dirname((__file__))+"/../input_data/demonetization-tweets.csv"	
    data = csv.DictReader(open(file_path, encoding="utf8"))
    print ("loading csv to mysql")
    tweets = list(data)
    set_analyzed_sentiment_to_data_set(tweets)
    clean_existing_table_data()
    sql_batch_insert(tweets)
    print ("Dumped csv data to mysql successfully...")

