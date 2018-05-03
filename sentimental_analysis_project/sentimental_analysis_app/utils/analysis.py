import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sentimental_analysis_app.utils.data_reader import read_csv_file
from sentimental_analysis_project.settings import NO_OF_REOCRDS_TO_PROCESS
from nltk.sentiment.util import *
from nltk import tokenize
import seaborn as sns

from indicoio import emotion, sentiment
import indicoio

indicoio.config.api_key = 'd7bc6d0cbc1083b4e6d24070648f5313'


data = read_csv_file()


from django.db import connection

def my_custom_sql():
    with connection.cursor() as cursor:
        cursor.execute("SELECT x FROM sentimental_analysis_app_demonitisationtweets WHERE tweet_id = 11")
        row = cursor.fetchone()

    return row

# Q1. What percentage of tweets is negative, positive or neutral?
def get_analized_sentiments():
    '''
    Utility function to classify the polarity of all the tweets using textblob.

    '''
    sid = SentimentIntensityAnalyzer()

    data['sentiment_compound_polarity']=data.text.apply(lambda x:sid.polarity_scores(x)['compound'])
    data['sentiment_neutral']=data.text.apply(lambda x:sid.polarity_scores(x)['neu'])
    data['sentiment_negative']=data.text.apply(lambda x:sid.polarity_scores(x)['neg'])
    data['sentiment_pos']=data.text.apply(lambda x:sid.polarity_scores(x)['pos'])

    data['sentiment_type']=''
    data.loc[data.sentiment_compound_polarity>0,'sentiment_type']='POSITIVE'
    data.loc[data.sentiment_compound_polarity==0,'sentiment_type']='NEUTRAL'
    data.loc[data.sentiment_compound_polarity<0,'sentiment_type']='NEGATIVE'

    return data[['sentiment_type']].to_dict()

#Q2. a. Get the most famous tweeted tweets
def get_most_famous_tweets():
    '''
    Utility function to classify the polarity of all the tweets using textblob.

    '''
    return data.iloc[data['favoriteCount'].argmax()]['text']


#Q2. b. Get the most famous re-tweeted tweets
def get_most_famous_retweets():
    '''
    Utility function to classify the polarity of all the tweets using textblob.

    '''
    return data.iloc[data['retweetCount'].argmax()]['text']


#Q3. The number of retweet per hour
def get_retweets_per_hour_count():
    data['hour'] = pd.DatetimeIndex(data['created']).hour
    tweets_hour = data.groupby(['hour'])['retweetCount'].sum()
    data['text_len'] = data['text'].str.len()
    tweets_all_hour = data.groupby(['hour'])['text_len'].sum()
    return tweets_all_hour, tweets_hour


def get_emotion(tweet_batch):
    emotions_list = []
    print (tweet_batch)
    response_list=indicoio.emotion(tweet_batch)
    for r in response_list:
        inverse = [(value, key) for key, value in r.items()]
        real_emotion = max(inverse)[1]
        emotions_list.append(real_emotion)
    return emotions_list


def process_batch(batch, n=1):
    l = len(batch)
    for ndx in range(0,l,n):
        yield batch[ndx:min(ndx+n,l)]

#Q4. Sentimental analysis of sowing percentage of emotions (joy, sad, fear etc.)
def get_emotion_to_x_map():
    # Note: To get the emotions out of tweets we are using paid service so limiting it to process all the records.
    tweets = data['text'][:NO_OF_REOCRDS_TO_PROCESS]
    X_to_text_map = {x:tweet for x,tweet in tweets.to_dict().items()}

    text_list = list(X_to_text_map.values())
    keys = list(X_to_text_map.keys())

    BATCH_SIZE = 100
    values = []
    for x  in process_batch(text_list,BATCH_SIZE):
        values.extend(get_emotion(list(x)))

    return dict(zip(keys, values))


#Q5. Get the twitter count group by device type like android, iphone etc.
def get_tweets_device_dict():
    data['Source'] = data.statusSource.str.split(r'\s*>\s*|\s*\</a>\s*').str[1]
    return (data['Source'].to_dict())

#Q6. Most popular N users.
def get_most_popular_users(count=10):
    print ("*********************")
    print (my_custom_sql())
    print ("*********************")
    data['TwtCnt'] = 1
    data_filtered_1 = data[['X', 'screenName', 'TwtCnt', 'retweetCount']]
    data_tweet = data_filtered_1.groupby(["screenName"]).sum().reset_index()
    result = data_tweet.sort_values('retweetCount', ascending=False).head(count)[['X', 'screenName', 'retweetCount', 'TwtCnt']]
    return result


#Q7. The Top N Users whose tweets generated most replies
def get_most_popular_users(count=10):
    data['Reply_Cnt'] = 1
    data_filtered_2 = data[['X', 'replyToSN', 'Reply_Cnt']]
    data_tweet_reply = data_filtered_2.groupby(["replyToSN"]).sum().reset_index()
    result = data_tweet_reply.sort_values('Reply_Cnt', ascending=False).head(10)[['X', 'replyToSN', 'Reply_Cnt']]
    return result

