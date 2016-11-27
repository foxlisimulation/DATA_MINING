import tweepy
consumer_key="wCzULA4zu6YvoxuCExL4YdvN6"
consumer_secret="OG39Xz2aFVgnFnH13GyRQ7wlupecBceaM3WOAShEvXzNcMCvzk"
acess_token="802824249584910336-65r5DbvkCqGFShUYW9l3xUCiueKCXXG"
acess_token_secret="mNYgXo1bRGIYW29oda7eE5lnmIWrGS1cvolKeWNJy5yan"
auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(acess_token,acess_token_secret)
api=tweepy.API(auth)
public_tweets=api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)
import os
output_filename=os.path.join(os.path.expanduser("~"),"data","twitter","python_tweets.json")
print(output_filename)
import json
with open(output_filename,'a') as output_file:
    search_results=api.search("python",rpp=100)
    s=json.JSONEncoder().encode(search_results)
    print(s)
    output_file.write(json.dumps(s))
    output_file.write("\n\n")

