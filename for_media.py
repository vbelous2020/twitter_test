import os
import shutil
import logging
import tweepy
from tweepy import OAuthHandler
from twitter_secret_key import consumer_key, consumer_secret
from os.path import expanduser
home = expanduser("~")


class TweetParser(object):
    def __init__(self):
        self.video_urls = []
        self.image_urls = []
        self.out_tweets = []
        self.api = None
        auth = OAuthHandler(consumer_key, consumer_secret)
        self.api = tweepy.API(auth, wait_on_rate_limit=True)   # This will make the rest of the code obey the rate limit

    def process_tweet_media(self, tweet):
        try:
            extended = tweet.extended_entities
            rv = []
            if not extended:
                rv.append("No media")
            if "media" in extended:
                for x in extended["media"]:
                    if x["type"] == "photo":
                        url = x["media_url"]
                        rv.append(url)
                    elif x["type"] in ["video", "animated_gif"]:
                        variants = x["video_info"]["variants"]
                        variants.sort(key=lambda a: a.get("bitrate", 0))
                        url = variants[-1]["url"].rsplit("?tag")[0]
                        rv.append(url)
            return rv
        except AttributeError:
            # logging.info("Extended entities not present in tweet")
            return []

    def save_data(self, video_urls, image_urls, account):
        self.video_urls = list(video_urls)
        self.image_urls = list(image_urls)
        logging.info("Saving image and video links to file")
        with open(os.path.join(account, "images.txt"), "w") as f:
            for url in image_urls:
                f.write(url + "\n")
        with open(os.path.join(account, "videos.txt"), "w") as f:
            for url in video_urls:
                f.write(url + "\n")

    def fetch(self, account, tweet_mode='extended', limit=3250):
        # 3250 tweets is max for parsing from each user
        dir_name = account
        api = self.api

        epoch = 1
        video_urls = set()
        image_urls = set()
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
        os.mkdir(dir_name)

        for tweet in tweepy.Cursor(api.user_timeline, id=account, tweet_mode=tweet_mode).items(limit):
            print("Tweets: {}".format(epoch))
            epoch += 1
            rv = self.process_tweet_media(tweet)
            for r in rv:
                if r.endswith("mp4"):
                    video_urls.add(r)
                else:
                    image_urls.add(r)
            id_tweet = tweet.id_str
            date_tweet = tweet.created_at
            text_tweet = tweet.full_text
            user_id = tweet.user.name
            self.out_tweets = [id_tweet, date_tweet, text_tweet, user_id, rv]
        self.save_data(video_urls, image_urls, account)


if __name__ == '__main__':
    users = ["AvakovArsen", "NatGeo", "disneyplus", "starwars", "IGN", "netflix", "Ukraine", "APUkraine", "Warcraft",
             "Wowhead", "ChristieGolden"]
    users2 = ["AvakovArsen"]
    parser = TweetParser()
    for user in users2:
        parser.fetch(user)

    # from TweetParser(so far useless) TODO or REMOVE
    # import wget
    # def download(self, urls, file_type, destination):
    #     self._download_from_urls("MAIN", list(urls), file_type, destination)
    #
    # def _download_from_urls(self, name, batch, file_type, dest_dir):
    #     for url in batch:
    #         logging.info("Thread: {} downloading {}".format(name, url))
    #         media_file = url.split("/")[-1]
    #         path = os.path.join(dest_dir, media_file)
    #         wget.download(url, path)
