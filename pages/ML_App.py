import streamlit as st
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from PIL import Image
import seaborn as sns
import sklearn
import configparser

# Twitter API configuration
config = configparser.RawConfigParser()
config.read('config.ini')

api_key = config['tweets']['api_key']
api_key_secret = config['tweets']['api_key_secret']
access_token = config['tweets']['access_token']
access_token_secret = config['tweets']['access_token_secret']
bearer_token = config['tweets']['bearer_token']

# Authentication for API v1.1
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

# Create Client object for API v2
client = tweepy.Client(bearer_token=bearer_token)

st.set_option('deprecation.showPyplotGlobalUse', False)

def app():
    st.title("Twitter Sentiment Analysis")

    activities = ["Tweet Analyzer", "Generate Twitter Data"]
    choice = st.sidebar.selectbox("Select Your Activity", activities)

    if choice == "Tweet Analyzer":
        st.subheader("Analyze the Tweets")
        st.write("1. Fetches recent Tweets from given handle")
        st.write("2. Generates a Word Cloud")
        st.write("3. Sentiment Analysis of Tweets and visualize them as graph")

        raw_text = st.text_area("Enter the Twitter handle")

        Analyzer_choice = st.selectbox("Select the Activities", ["Show Recent Tweets", "Generate WordCloud", "Visualize the Sentiment Analysis"])

        if st.button("Analyze"):
            if Analyzer_choice == "Show Recent Tweets":
                st.success("Fetching last 5 Tweets")
                recent_tweets = show_recent_tweets(raw_text)
                st.write(recent_tweets)
            elif Analyzer_choice == "Generate WordCloud":
                st.success("Generating Word Cloud")
                img = gen_wordcloud(raw_text)
                st.image(img)
            else:
                df = plot_analysis(raw_text)
                st.write(sns.countplot(x=df["Analysis"], data=df))
                st.pyplot(fig=None)
                st.set_option('deprecation.showPyplotGlobalUse', False)
    else:
        st.subheader("Fetches the last 100 tweets from the twitter handle & performs some tasks")
        st.write("1. Converts Tweet into a DataFrame")
        st.write("2. Performs cleaning of Tweets")
        st.write("3. Analyzes Subjectivity of tweets")
        st.write("4. Analyzes Polarity of tweets")
        st.write("5. Analyzes Sentiments of tweets")

        user_name = st.text_area("*Enter the Twitter handle (without @)*")

        if st.button("Show Data"):
            st.success("Fetching Last 100 Tweets")
            df = get_data(user_name)
            st.write(df)

    st.subheader("-------------------------------Made by @Akash-------------------------")

def show_recent_tweets(raw_text):
    user = client.get_user(username=raw_text)
    user_id = user.data.id
    posts = client.get_users_tweets(id=user_id, max_results=100, tweet_fields=['lang', 'created_at'], expansions='author_id')
    return [tweet.text for tweet in posts.data[:5] if tweet.lang == 'en']

def gen_wordcloud(raw_text):
    user = client.get_user(username=raw_text)
    user_id = user.data.id
    posts = client.get_users_tweets(id=user_id, max_results=100, tweet_fields=['lang', 'created_at'], expansions='author_id')
    df = pd.DataFrame([tweet.text for tweet in posts.data], columns=['Tweets'])
    allWords = ' '.join([twts for twts in df['Tweets']])
    wordCloud = WordCloud(width=500, height=300, random_state=21, max_font_size=110).generate(allWords)
    plt.imshow(wordCloud, interpolation="bilinear")
    plt.axis('off')
    plt.savefig('WC.jpg')
    return Image.open("WC.jpg")

def plot_analysis(raw_text):
    user = client.get_user(username=raw_text)
    user_id = user.data.id
    posts = client.get_users_tweets(id=user_id, max_results=100, tweet_fields=['lang', 'created_at'], expansions='author_id')
    df = pd.DataFrame([tweet.text for tweet in posts.data], columns=['Tweets'])

    def cleanTxt(text):
        text = re.sub('@[A-Za-z0–9]+', '', text) # Removing @mentions
        text = re.sub('#', '', text) # Removing '#' hash tag
        text = re.sub('RT[\s]+', '', text) # Removing RT
        text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
        return text

    df['Tweets'] = df['Tweets'].apply(cleanTxt)
    df['Subjectivity'] = df['Tweets'].apply(lambda text: TextBlob(text).sentiment.subjectivity)
    df['Polarity'] = df['Tweets'].apply(lambda text: TextBlob(text).sentiment.polarity)
    df['Analysis'] = df['Polarity'].apply(lambda score: 'Positive' if score > 0 else ('Neutral' if score == 0 else 'Negative'))

    return df

def get_data(user_name):
    user = client.get_user(username=user_name)
    user_id = user.data.id
    posts = client.get_users_tweets(id=user_id, max_results=100, tweet_fields=['lang', 'created_at'], expansions='author_id')
    df = pd.DataFrame([tweet.text for tweet in posts.data], columns=['Tweets'])

    def cleanTxt(text):
        text = re.sub('@[A-Za-z0–9]+', '', text) # Removing @mentions
        text = re.sub('#', '', text) # Removing '#' hash tag
        text = re.sub('RT[\s]+', '', text) # Removing RT
        text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
        return text

    df['Tweets'] = df['Tweets'].apply(cleanTxt)
    df['Subjectivity'] = df['Tweets'].apply(lambda text: TextBlob(text).sentiment.subjectivity)
    df['Polarity'] = df['Tweets'].apply(lambda text: TextBlob(text).sentiment.polarity)
    df['Analysis'] = df['Polarity'].apply(lambda score: 'Positive' if score > 0 else ('Neutral' if score == 0 else 'Negative'))

    return df

if __name__ == "__main__":
    app()
