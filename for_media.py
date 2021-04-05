import logging
import shutil
import os
import tweepy
from twitter_secret_key import consumer_key, consumer_secret, access_key, access_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


def fetch(self, account, tweet_mode='extended', limit=None):
    dir_name = account
    api = self.api
    epoch = 1
    video_urls = set()
    image_urls = set()
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    os.mkdir(dir_name)

    for tweet in tweepy.Cursor(api.user_timeline, id=account, tweet_mode=tweet_mode).items(limit):
        print("Epoch: {}".format(epoch))
        epoch += 1
        rv = self.process_tweet(tweet)
        for r in rv:
            if r.endswith("mp4"):
                video_urls.add(r)
            else:
                image_urls.add(r)


def process_tweet(self, tweet):
    try:
        extended = tweet.extended_entities
        if not extended:
            return []
        rv = []
        if "media" in extended:
            for x in extended["media"]:
                if x["type"] == "photo":
                    url = x["media_url"]
                    rv.append(url)
                elif x["type"] in ["video", "animated_gif"]:
                    variants = x["video_info"]["variants"]
                    variants.sort(key=lambda x: x.get("bitrate", 0))
                    url = variants[-1]["url"].rsplit("?tag")[0]
                    rv.append(url)
        return rv
    except AttributeError:
        logging.error("Extended entities not present in tweet")
        return []


if __name__ == '__main__':
    pass