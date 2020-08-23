from flask import Flask,render_template,url_for,request,redirect
import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 
#constructor takes the name of current module 
app = Flask(__name__)

class TwitterClient(object): 
    ''' 
    Generic Twitter Class for sentiment analysis. 
    '''
    def __init__(self): 
        ''' 
        Class constructor or initialization method. 
        '''
        # keys and tokens from the Twitter Dev Console 
        consumer_key = 'xChc29fnbYFlcN7h9aphDF4Sl'
        consumer_secret = 'sPXq6werxV8kn0IIasW3WlxhWrEPZHuOFIVNsafqmQKa2c3YG4'
        access_token = '1073390408179187712-SN3YOw4xJ4xVDNHmp2BK4DG9hZnjmW'
        access_token_secret = 'bTGidywGLmiGzNwAz6O2GgjrY45C0UaIMDb7AKIRPRWUF'
  
        # attempt authentication 
        try: 
            # create OAuthHandler object 
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            # set access token and secret 
            self.auth.set_access_token(access_token, access_token_secret) 
            # create tweepy API object to fetch tweets 
            self.api = tweepy.API(self.auth) 
        except: 
            print("Error: Authentication Failed")
    def get_tweets(self, query, count = 10): 
        ''' 
        Main function to fetch tweets and parse them. 
        '''
        # empty list to store parsed tweets 
        tweets = []
      
  
        try: 
            # call twitter api to fetch tweets 
            fetched_tweets = self.api.search(q = query, count = count) 
  
            # parsing tweets one by one 
            for tweet in fetched_tweets: 
                # empty dictionary to store required params of a tweet 
                parsed_tweet = {} 
  
                # saving text of tweet 
                parsed_tweet['text'] = tweet.text
            
                # saving sentiment of tweet 
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 
  
                # appending parsed tweet to tweets list 
                if tweet.retweet_count > 0: 
                    # if tweet has retweets, ensure that it is appended only once 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet)
            # storing the retrived tweets from twitter API into a file called twitter
            fp = open("mouni.txt","a",encoding='utf-8')
            for tweet in tweets:
                fp.write(str(tweet['text']))
            fp.close()
    
            return tweets 
  
        except tweepy.TweepError as e: 
            # print error (if any) 
            print("Error : " + str(e)) 
  
    def clean_tweet(self, tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) (\w+:\/\/\S+)", " ", tweet).split()) 
  
    def get_tweet_sentiment(self, tweet): 
        ''' 
        Utility function to classify sentiment of passed tweet 
        using textblob's sentiment method 
        '''
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(self.clean_tweet(tweet)) 
        # set sentiment 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'
  
    
  
def main(query,count): 
    # creating object of TwitterClient Class 
    api = TwitterClient() 
    # calling function to get tweets 
    tweets = api.get_tweets(query = query, count = count)
    print('tweets')
    # picking positive tweets from tweets 
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
    # percentage of positive tweets
    positive = 100*len(ptweets)/len(tweets) 
    # picking negative tweets from tweets 
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
    # percentage of negative tweets
    negitive = 100*len(ntweets)/len(tweets)
    # percentage of neutral tweets
    neutral = 100*(len(tweets)-len(ntweets)-len(ptweets))/len(tweets)
    # storing first 5 positive and negative tweets  into tweets file
    fp = open("tweets.txt","a",encoding='utf-8')
    for tweet in ptweets:
        
        fp.write(str(tweet['text']))
    fp.close()
    return [positive,negitive,neutral]
  



# route is a decorator, which tells the application which URL should call the associated function.
@app.route('/')
@app.route('/home')
# rendering of home.html from python program
def home():
    return render_template('home.html')

@app.route('/submit',methods=['POST'])
def mysubmission():
    T =request.form['t1']
    C =request.form['t2']
    print(T,C)
    if not (T or C ):
        print("t or c")
        return redirect(url_for('home'))
    if ((type(T) == str) and (C.isdigit())):
        print("type")
        positive,negitive,neutral = main(T,int(C))
        return render_template('output.html',positive=positive,negitive= negitive,neutral= neutral)
    return redirect(url_for('home'))
    


# Runnig of server
if __name__ == '__main__':
    app.run(host='localhost',port=8000)
