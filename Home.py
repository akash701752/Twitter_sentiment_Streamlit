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
import streamlit as st
from streamlit_option_menu import option_menu
import json
from streamlit_lottie import st_lottie

# 1=sidebar menu, 2=horizontal menu, 3=horizontal menu w/ custom menu
EXAMPLE_NO = 1

def streamlit_menu(example=1):
    if example == 1:
        # 1. as sidebar menu
        with st.sidebar:
            selected = option_menu(
                menu_title="Main Menu",  
                options=["Home", "Analysis", "Tweet Data"],  
                icons=["house", "book", "graph-down-arrow"], 
                menu_icon="cast",  
                default_index=0,  
            )
        return selected

    if example == 2:
        # 2. horizontal menu w/o custom style
        selected = option_menu(
            menu_title=None,  
            options=["Home", "Projects", "Contact"], 
            icons=["house", "book", "envelope"],  
            menu_icon="cast",  
            default_index=0, 
            orientation="horizontal",
        )
        return selected

    if example == 3:
        # 2. horizontal menu with custom style
        selected = option_menu(
            menu_title=None,  
            options=["Home", "Projects", "Contact"], 
            icons=["house", "book", "envelope"],  
            menu_icon="cast",  
            default_index=0, 
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {
                    "font-size": "25px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "green"},
            },
        )
        return selected

st.title(f"Twitter Sentiment Analysis")
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# def load_lottieurl(url: str):
#     r = requests.get(url)
#     if r.status_code != 200:
#         return None
#     return r.json()

lottie_twitter = load_lottiefile("lottiefile/twitter.json")  
# lottie_hello = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_M9p23l.json")

st_lottie(
    lottie_twitter,
    speed=1,
    reverse=False,
    loop=True,
    quality="low", # medium ; high
    # renderer="svg", # canvas
    height='500px',
    width='450px',
    key=None,
)

selected = streamlit_menu(example=EXAMPLE_NO)

if selected == "Home":
    st.write("Sentiment Analysis is contextual mining of text which identifies and extracts subjective information in source material, and helping a business to understand the social sentiment of their brand, product or service while monitoring online conversations." )

    st.write("Analysis of social media streams is usually restricted to just basic sentiment analysis and count based metrics. This is akin to just scratching the surface and missing out on those high value insights that are waiting to be discovered. So what should a brand do to capture that low hanging fruit?")

    st.write("With the recent advances in deep learning, the ability of algorithms to analyse text has improved considerably. Creative use of advanced artificial intelligence techniques can be an effective tool for doing in-depth research.")
if selected == "Analysis":
    st.title(f"Tweet Analysis ")
    st.write("Tweet Sentiment Analysis is basically extraction of tweets from one's Twitter account and then perform data extraction from tweets using various Machine Learning Algorithms" )

    st.write("After successful data cleaning of tweets. Tweets are analysed using Natural Language Processing and assign Polarity and Subjectivity to the tweets and determine the sentiments of tweets")

    st.write("After analysis we can visualize the sentiments in the from of Charts or wordcloud which tells us about the words which are used by the person most frequently.")
if selected == "Tweet Data":
    st.title(f"Tweet Data ")
    st.write("In tweet analysis, Twitter data is used to study and understand the sentiments, opinions, and emotions of users on various topics. This data can be collected through the Twitter API and analyzed using various techniques such as natural language processing, text mining, and machine learning.")
    st.write("The data can be used to track the spread of information, identify influencers, and monitor brand mentions.")

st.subheader("------------------------- Developed by @Akash ---------------------       ")