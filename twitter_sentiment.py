import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 

class TwitterClient(object): 
    def __init__(self): 
        ConsumerKey = '***********'
        ConsumerSecret = '************'
        AccessToken = '****************'
        AccessTokenSecret = '***************'
        
        try:  
            self.auth = OAuthHandler(ConsumerKey, ConsumerSecret)  
            self.auth.set_access_token(AccessToken, AccessTokenSecret) 
            self.api = tweepy.API(self.auth) 
        except: 
            print("Error: Authentication Failed") 

    def clean_tweet(self, tweet): 
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) 
                                    |(\w+:\/\/\S+)", " ", tweet).split()) 

    def get_tweet_sentiment(self, tweet): 
                               
        tweet_sample = TextBlob(self.clean_tweet(tweet))  
        if tweet_sample.sentiment.polarity > 0: 
            return 'positive'
        elif tweet_sample.sentiment.polarity < 0: 
            return 'negative'
        else: 
            return 'neutral'

    def get_tweets(self, topic, count = 10):  
        tweets = [] 

        try:  
            fetched_tweets = self.api.search(q = topic, count = count)  
            for each_tweet in fetched_tweets: 
                parsed_tweet = {} 
                parsed_tweet['text'] = each_tweet.text 
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(each_tweet.text)  
                if each_tweet.retweet_count > 0: 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 

            return tweets 

        except tweepy.TweepError as e: 
            print("Error : " + str(e)) 

def sentimentHelper(): 
    Tweet_api = TwitterClient()  
    tweets = Tweet_api.get_tweets(topic = 'cppsecrets.com', count = 50) 
    
    positive_tweets = [each_tweet for each_tweet in tweets if each_tweet['sentiment'] == 'positive'] 
    print(f"The Overall Positive tweets percentage are {(100*len(positive_tweets)/len(tweets))} %") 
    neutral_tweets = [each_tweet for each_tweet in tweets if each_tweet['sentiment'] == 'neutral']
    print(f"The Overall Neutral tweets percentage are {(100*len(neutral_tweets)/len(tweets))} %") 
    print(f"The Overall Negative tweets percentage are {(100*(len(tweets) -  (len(positive_tweets) + len(neutral_tweets))/len(tweets))} %")
    
    # Please Uncomment the following lines if you want to print your 
    # positive , negative or neutral tweets.
                                                           
    # print("\n\nPositive tweets:")
    # if (len(positive_tweets) < 10):
    #     for tweet in positive_tweets: 
    #         print(tweet['text'])
    # else:
    #     for tweet in positive_tweets[:10]: 
    #         print(tweet['text'])
   
    # print("\n\nNegative tweets:")
    # if (len(negative_tweets) < 10):
    #     for tweet in negative_tweets: 
    #         print(tweet['text'])
    # else:
    #     for tweet in negative_tweets[:10]: 
    #         print(tweet['text'])
    
    # print("\n\nNeutral tweets:")
    # if (len(neutral_tweets) < 10):
    #     for tweet in neutral_tweets: 
    #         print(tweet['text'])
    # else:
    #     for tweet in neutral_tweets[:10]:
    #         print(tweet['text'])
            
if __name__ == "__main__": 
	sentimentHelper()