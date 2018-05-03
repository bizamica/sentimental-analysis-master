from django.shortcuts import render,HttpResponse
import json
from django.shortcuts import redirect
from django.conf import settings
from sentimental_analysis_app.models import DemonitisationTweets
from sentimental_analysis_app.utils.data_writer import dump_csv_data_to_db
from django.db.models import Count
from django.core import serializers
from django.db import connection
from contextlib import closing

 
def profile(request):
    if not request.user.is_authenticated:
        return redirect('/')

    return render(request,'home.html')

def get_total_of_db_records():
    sql = "SELECT count(*) as total FROM sentimental_analysis_app_demonitisationtweets;"
    total = 0
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        rows = cursor.fetchone()
        total = rows[0]
    return total

def process_data(request):
    print ("*****************Processing the CSV data**************************")
    # dump csv data to sqlite DB
    dump_csv_data_to_db()

    return HttpResponse(content=json.dumps({"message":"Successfully processed CSV data...!!!"}),content_type="application/json")

# Q1. Get percentage of different type of sentiment (Positive, Negative, Neutral)
def get_percentages_of_different_sentiments(request):
    chartData = []
    total = get_total_of_db_records()
    sql = "SELECT sentiment_type, count(*) as total FROM sentimental_analysis_app_demonitisationtweets GROUP BY sentiment_type;"
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            percentage = round((row[1]/total)*100,2)
            chartData.append([row[0], percentage])
    return HttpResponse(content=json.dumps({'chartData':chartData, 'chartTitle': "<center><h2>Percentage of Tweets Positive, Negative or Netural.</h2></center>"}), content_type="application/json")


# Q2. Get the most famous tweets
def get_most_famous_tweets(request):
    chartData = []
    sql = "SELECT x, screen_name, text, favorite_count FROM  sentimental_analysis_app_demonitisationtweets ORDER BY favorite_count DESC limit 10;"
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            chartData.append({"id":row[0],"screenName":row[1],"text":row[2],"famousCount":row[3]})
    return HttpResponse(content=json.dumps({'chartData':chartData, 'chartTitle': "<center><h2>Showing Get the most famous tweets.</h2></center>"}), content_type="application/json")

# Q2. Get the most re-tweeted tweets
def get_most_re_tweeted_tweets(request):
    chartData = []
    sql = "SELECT x, screen_name, text, retweet_count FROM  sentimental_analysis_app_demonitisationtweets ORDER BY retweet_count DESC limit 10;"
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            chartData.append({"id":row[0],"screenName":row[1],"text":row[2],"retweetCount":row[3]})
    return HttpResponse(content=json.dumps({'chartData':chartData, 'chartTitle': "<center><h2>Showing Get the most re-tweeted tweets.</h2></center>"}), content_type="application/json")


#Q3. Create stacked chart (Retweets, Total Tweets) showing “‘Hour of the Day Trends” TweetCount Vs Hour.
def get_tweets_vs_retweet_hour_wise(request):
    # Get Total no of Tweets hour wise
    total_tweets = ['TotalTweets']
    initial_values = [0 for i in range(0,25)]
    total_tweets.extend(initial_values)
    total_tweets_sql = "SELECT hour, count(text) as TotalTweets FROM sentimental_analysis_app_demonitisationtweets GROUP BY hour ORDER BY hour ASC;"
    with closing(connection.cursor()) as cursor:
        cursor.execute(total_tweets_sql)
        rows = cursor.fetchall()
        for row in rows:
            total_tweets[row[0]+1] = row[1]
        # complete the cycle 0 means 24
        total_tweets[24+1] = total_tweets[1]
    # Get count of reTweets hour wise
    re_tweets = ['Retweets']
    re_tweets.extend(initial_values)
    re_tweets_sql = "SELECT hour, count(text) as ReTweets FROM sentimental_analysis_app_demonitisationtweets WHERE is_retweet=True group by hour ORDER BY hour ASC;"
    with closing(connection.cursor()) as cursor:
        cursor.execute(re_tweets_sql)
        rows = cursor.fetchall()
        for row in rows:
            re_tweets[row[0]+1] =row[1]
        # complete the cycle 0 means 24
        re_tweets[24+1] = re_tweets[1]
    chartData = [total_tweets, re_tweets]

    return HttpResponse(content=json.dumps({'chartData':chartData, 'chartTitle': "<center><h2>3. Hour of the Day Trends</h2></center>"}), content_type="application/json")



# Q4. Get percentage of different type of emotions (Joy, Sad, Fear etc.)
def get_percentages_of_different_emotions(request):
    total = get_total_of_db_records()
    chartData = []
    sql = "SELECT emotions, count(*) as total FROM sentimental_analysis_app_demonitisationtweets WHERE emotions!='NULL' GROUP BY emotions ORDER BY emotions ASC;"
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            percentage = round((row[1]/total)*100,2)
            chartData.append([row[0],percentage])
    return HttpResponse(content=json.dumps({'chartData':chartData, 'chartTitle': "<center><h2>Percentage of emotions (Note: Currently processing only 5000 records because we are using paid service)</h2></center>"}), content_type="application/json")


# Q5. Create Bar chart showing Tweet counts Device wise (twitter for Android, twitter Web client, Twitter for iPhone, Facebook, Twitter for iPad, etc.)
def get_tweet_counts_device_wise(request):
    chartData = []
    sql = "SELECT device_type, count(*) as total FROM sentimental_analysis_app_demonitisationtweets GROUP BY device_type ORDER BY total DESC limit 10;"
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            chartData.append([row[0],row[1]])
    return HttpResponse(content=json.dumps({'chartData':chartData, 'chartTitle': "<center><h2>Showing Tweet counts Device wise (twitter for Android, twitter Web client etc.)</h2></center>"}), content_type="application/json")

#Q6. Get most popular Users
def get_most_popular_users_chart_data(request):
    chartData = []
    sql = "SELECT screen_name, sum(retweet_count) as reTweetCount, count(screen_name) as tweet FROM sentimental_analysis_app_demonitisationtweets GROUP BY screen_name ORDER BY sum(retweet_count) DESC limit 10;"
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()
        sr_no = 1
        for row in rows:
            chartData.append({"id":sr_no,"screenName":row[0],"retweetCount":str(row[1]),"tweetCount":str(row[2])})
            sr_no+=1
    return HttpResponse(content=json.dumps({'chartData':chartData, 'chartTitle': "<center><h2>6. Most Popular 10 Users</h2></center>"}), content_type="application/json")


#Q7. Get Users whose tweets generated most replies.
def get_users_with_most_replies(request):
    chartData = []
    sql = "SELECT reply_to_sn, count(screen_name) as RepliesReceived FROM sentimental_analysis_app_demonitisationtweets WHERE reply_to_sn!='NA' GROUP BY reply_to_sn ORDER BY RepliesReceived DESC limit 10;"
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()
        sr_no = 1
        for row in rows:
            chartData.append({"id":sr_no,"user":row[0],"repliesReceived":str(row[1])})
            sr_no+=1
    return HttpResponse(content=json.dumps({'chartData':chartData, 'chartTitle': "<center><h2>7. Get Users whose tweets generated most replies.</h2></center>"}), content_type="application/json")
