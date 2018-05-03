from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from sentimental_analysis_app import views
urlpatterns = [
    url(r'^$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^accounts/profile/$', views.profile, name='profile'),
    url(r'^processdata/$', views.process_data, name='processdata'),
    url(r'^admin/', admin.site.urls),
    url(r'^q1/$', views.get_percentages_of_different_sentiments, name='Q1'),
    url(r'^q2/$', views.get_most_famous_tweets, name='Q2'),
    url(r'^q3/$', views.get_tweets_vs_retweet_hour_wise, name='Q3'),
    url(r'^q2b/$', views.get_most_re_tweeted_tweets, name='Q2-b'),
    url(r'^q4/$', views.get_percentages_of_different_emotions, name='Q4'),
    url(r'^q5/$', views.get_tweet_counts_device_wise, name='Q5'),
    url(r'^q6/$', views.get_most_popular_users_chart_data, name='Q6'),
    url(r'^q7/$', views.get_users_with_most_replies, name='Q7'),
]