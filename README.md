# Emotion Recognition in Text (Indonesian)

Emotion Recognition Analysis - part of Natural Language Processing (NLP) which is similar to sentiment analysis. It aims to identify the human emotion in a written text.
This repo use text data retrieved from Twitter using Twitter Streaming API. While the analysis itself using keywords-based approach. 

Please visit my Medium article [here](https://riorizkiaryanto.medium.com/emotion-analysis-for-topic-mudik-during-covid-19-pandemic-56d19bc61aa1) where I explained one of real case that I did using these codes. 

## How to use the codes
1. Put the credentials related to your Twitter API in the *credential.py* file. Put as well the credential for the MySQL database. The database will be used to stored the retrieved tweets from the API
2. Edit the *settings.py* file. This file contain what keyword that you wanted to retrieved the data from Twitter. Also put the table name where you want to store the collected data in the MySQL database
3. Run *emotion.py* file to retrieve the Tweets from Twitter, and also run the emotion recognition analysis