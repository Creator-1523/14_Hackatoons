# -*- coding: utf-8 -*-
"""Sentimental.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1etFRcP20NGoIL7llnAMEijYYv_LICZ20
"""

# import the libraries
import numpy as np
import pandas as pd
import re

import matplotlib.pyplot as plt
from textblob import TextBlob
from nltk.stem import WordNetLemmatizer
def senti():
    df=pd.read_csv("Bitcoin_tweets.csv")
    # df.head()

    # remove nan value row in hastags column
    df. dropna(subset = ["hashtags"], inplace=True)
    # df.head(5)

    # total value size
    print("Tweet Size: ", len(df))

    # get only texts
    df = df[['text']]
    df.columns = ['tweets']

    # create a function to clean the tweets
    def cleanTwt(twt):
        twt = re.sub("#bitcoin", 'bitcoin', twt) # removes the '#' from bitcoin
        twt = re.sub("#Bitcoin", 'Bitcoin', twt) # removes the '#' from Bitcoin
        twt = re.sub('#[A-Za-z0-9]+', '', twt) # removes any string with a '#'
        twt = re.sub('\\n', '', twt) # removes the '\n' string
        twt = re.sub('https:\/\/\S+', '', twt) # removes any hyperlinks
        return twt

    df['cleaned_tweets'] = df['tweets'].apply(cleanTwt)
    # df

    # create a function to get subjectivity
    def getSubjectivity(twt):
        return TextBlob(twt).sentiment.subjectivity

    # create a function to get the polarity
    def getPolarity(twt):
        return TextBlob(twt).sentiment.polarity

    # create two new columns called "Subjectivity" & "Polarity"
    df['subjectivity'] = df['cleaned_tweets'].apply(getSubjectivity)
    df['polarity'] = df['cleaned_tweets'].apply(getPolarity)

    # df.head(5)

    # create a function get the sentiment text
    def getSentiment(score):
        if score < 0:
            return "negative"
        elif score == 0:
            return "neutral"
        else:
            return "positive"

    # create a column to store the text sentiment
    df['sentiment'] = df['polarity'].apply(getSentiment)

    # show the data
    # df.head()

    # Let's preprocess the tweets

    # import nltk

    import nltk
    nltk.download('stopwords')
    from nltk.corpus import stopwords
    STOPWORDS = set(stopwords.words('english'))
    # Import nltk stopwords and customize it to add common crypto words that don't add too much information
    stopwords = nltk.corpus.stopwords.words('english')
    crypto_words = ['btc','bitcoin','eth','etherum','crypto']

    stopwords = stopwords + crypto_words

    def preprocess_tweet(tweet, stopwords):

        tweet = tweet.lower()

        tweet = tweet.replace('\n\n',' ')

        # remove english stopwords
        tweet = ' '.join([word for word in tweet.split() if word not in stopwords])

        # regular expression that preprocess tweets
        tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ", tweet).split())

        return tweet

    # create a scatter plot to show the subjectivity and the polarity
    plt.figure(figsize=(14,10))

    for i in range(0, 2000):
        plt.scatter(df["polarity"].iloc[[i]].values[0], df["subjectivity"].iloc[[i]].values[0], color="Purple")
    plt.title("Scatter")
    plt.title("Sentiment Analysis Scatter Plot")
    plt.xlabel('polarity')
    plt.ylabel('subjectivity')
    plt.savefig(r"C:\Users\Shaun\Desktop\PBL Mineral\Prypto\Prypto_venv\static\predict\Scatter.png",facecolor='white', transparent=True,  bbox_inches='tight')
    plt.close()
    # plt.show()

    # create a bar chart to show the cout of Positive, Neutral and Nehative sentiments
    df['sentiment'].value_counts().plot(kind="bar")
    plt.title("Sentiment Analysis Scatter Plot")
    plt.xlabel("Polarity")
    plt.ylabel("Subjectivity")
    plt.savefig(r"C:\Users\Shaun\Desktop\PBL Mineral\Prypto\Prypto_venv\static\predict\Bar.png",facecolor='white', transparent=True,  bbox_inches='tight')
    plt.close()

