
import mysql.connector
import pandas as pd
import re
import nltk
import json
import settings
import credential
from collections import Counter
from langdetect import detect
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream
from textblob import TextBlob

def langDetect(item):
    try:
        return detect(item)
    except:
        return None

def clean_tweet(tweet):
    '''
    Use sumple regex statemnents to clean tweet text by removing links and special characters
    '''
    text =  ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    return re.sub("^RT\s?", '', text.strip())

def deEmojify(text):
    '''
    Strip all non-ASCII characters to remove emoji characters
    '''
    if text:
        return text.encode('ascii', 'ignore').decode('ascii')
    else:
        return None

def bagWords(item):
    result = []

    # found word started with capitalize letter
    capitalize = re.findall('[A-Z][a-z]+', item)
    capitalize = [cap.lower() for cap in capitalize]

    # word tokenize
    bagOfWords = item.lower().split()

    # remove if word is digit
    bagOfWords = [value for value in bagOfWords if value.isdigit() is False]
    n_bagOfWords = len(bagOfWords)

    # insert bigram into bag of words
    if n_bagOfWords != 0:
        bigram = list(nltk.ngrams(bagOfWords, 2))
        for item in bigram:
            bagOfWords.append(item[0] + " " + item[1])
        # extend bag of word with capitalize word
        if capitalize != []:
            bagOfWords.extend(capitalize)
        else:
            pass

    if bagOfWords == [] and capitalize != []:
        result.extend(capitalize)
    else:
        result.extend(bagOfWords)
    return result

def sim(listA, reference):
    if listA != []:
        result = {}
        # count word occurrences
        a_vals = Counter(listA)
        for key in reference:
            listB = reference[key]
            b_vals = Counter(listB)

            # convert to word-vectors
            # convert to word-vectors
            words  = list(a_vals.keys() | b_vals.keys())
            a_vect = [a_vals.get(word, 0) for word in words]
            b_vect = [b_vals.get(word, 0) for word in words]

            # find cosine similiarity
            len_a  = sum(av*av for av in a_vect) ** 0.5
            len_b  = sum(bv*bv for bv in b_vect) ** 0.5
            dot    = sum(av*bv for av,bv in zip(a_vect, b_vect))
            cosine = dot / (len_a * len_b)
            result[key] = cosine

        if max(result.values()) != 0:
            return [result, max(result, key=result.get)]
        else:
            return [result, "unknown"]
    else:
        result = {}
        for key in reference:
            result[key] = 0
        return [result, "unknown"]

class MyStreamListener(StreamListener):
    '''
    Tweets are known as “status updates”. So the Status class in tweepy has properties describing the tweet.
    https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object.html
    '''

    def on_status(self, status):
        '''
        Extract info from tweets
        '''

        if status.retweeted:
            # Avoid retweeted info, and only original tweets will be received
            return True
        # Extract attributes from each tweet
        id_str = status.id_str
        created_at = status.created_at
        text = deEmojify(status.text).replace("\n"," ")  # Pre-processing the text
        sentiment = TextBlob(text).sentiment
        polarity = sentiment.polarity
        subjectivity = sentiment.subjectivity

        user_name = status.user.name
        user_screen_name = status.user.screen_name
        user_created_at = status.user.created_at
        user_location = deEmojify(status.user.location)
        user_description = deEmojify(status.user.description)
        user_followers_count = status.user.followers_count
        longitude = None
        latitude = None
        if status.coordinates:
            longitude = status.coordinates['coordinates'][0]
            latitude = status.coordinates['coordinates'][1]

        retweet_count = status.retweet_count
        favorite_count = status.favorite_count

        lang = langDetect(clean_tweet(text))
        emotion = sim(bagWords(clean_tweet(text)), dictRef)[1]
        print(text)
        print(lang, emotion)
        print("=======")

        # Store all data in MySQL
        if mydb.is_connected():
            mycursor = mydb.cursor()
            sql = "INSERT INTO {} (id_str, created_at, text, polarity, subjectivity, user_name, user_screen_name, " \
                  "user_created_at, user_location, user_description, user_followers_count, longitude, latitude, " \
                  "retweet_count, favorite_count, lang, emotion) VALUES " \
                  "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE " \
                  "created_at=values(created_at)," \
                  "text=values(text)," \
                  "polarity=values(polarity)," \
                  "subjectivity=values(subjectivity)," \
                  "user_name=values(user_name)," \
                  "user_screen_name=values(user_screen_name)," \
                  "user_created_at=values(user_created_at)," \
                  "user_location=values(user_location)," \
                  "user_description=values(user_description)," \
                  "user_followers_count=values(user_followers_count)," \
                  "longitude=values(longitude)," \
                  "latitude=values(latitude)," \
                  "retweet_count=values(retweet_count)," \
                  "favorite_count=values(favorite_count)," \
                  "lang=values(lang)," \
                  "emotion=values(emotion)".format(
                settings.TABLE_NAME)
            val = (int(id_str), created_at, text, polarity, subjectivity, user_name, user_screen_name,
                   user_created_at, user_location, user_description, user_followers_count,
                   longitude, latitude, retweet_count, favorite_count, lang, emotion)
            mycursor.execute(sql, val)
            mydb.commit()
            mycursor.close()

try:
    with open('source/ref.json') as file:
        dictRef = json.load(file)

    # connect to mysql db
    mydb = mysql.connector.connect(
        host="localhost",
        # port="8081",
        # unix_socket = 'localhost:/Applications/MAMP/tmp/mysql/mysql.sock',
        user="rio",
        passwd="riodb",
        database="twitterdb",
        charset='utf8'
    )
    if mydb.is_connected():
        '''
        Check if this table exits. If not, then create a new one.
        '''
        mycursor = mydb.cursor()
        mycursor.execute("""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_name = '{0}'
            """.format(settings.TABLE_NAME))
        if mycursor.fetchone()[0] != 1:
            mycursor.execute("CREATE TABLE {} ({})".format(settings.TABLE_NAME, settings.TABLE_ATTRIBUTES))
            mydb.commit()
        mycursor.close()

    # This handles Twitter auth and the connection to Twitter Streaming API
    l = MyStreamListener()
    auth = OAuthHandler(credential.api_key, credential.api_secret_key)
    auth.set_access_token(credential.access_token, credential.access_token_secret)
    stream = Stream(auth, l)

    # This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    try:
        stream.filter(track=settings.TRACK_WORDS)
    except:
        pass
except:
    pass