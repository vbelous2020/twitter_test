import os
import shutil
import logging
import tweepy
import csv
from tweepy import OAuthHandler
from os.path import expanduser
from twitter_secret_key import consumer_key, consumer_secret
from db_funcs import save_all_to_db, save_user_to_db
home = expanduser("~")


class TweetParser(object):
    def __init__(self):
        self.user_data = []
        self.out_tweets = []
        self.video_urls = []
        self.image_urls = []
        self.api = None
        auth = OAuthHandler(consumer_key, consumer_secret)
        self.api = tweepy.API(auth, wait_on_rate_limit=True)  # This will make the rest of the code obey the rate limit

    def fetch_user(self, account):
        api = self.api
        twitter_user = api.get_user(account)
        username = twitter_user.screen_name
        followers_count = twitter_user.followers_count
        location = twitter_user.location
        registration_date = twitter_user.created_at
        user_data = ([username, followers_count, location, registration_date])
        self.user_data = user_data
        save_user_to_db(user_data)

    def save_data(self, video_urls, image_urls, out_tweets, account):
        self.video_urls = list(video_urls)
        self.image_urls = list(image_urls)
        print("Saving all data from tweets. \n")
        logging.info("Saving image and video links to files.")
        with open(os.path.join(account, "images.txt"), "w") as f:
            for url in image_urls:
                f.write(url + "\n")
        with open(os.path.join(account, "videos.txt"), "w") as f:
            for url in video_urls:
                f.write(url + "\n")
        # save to DB
        save_all_to_db(out_tweets)
        # save to CSV
        with open('%s_tweets.csv' % account, 'w', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["user", "id", "created_at", "text", "location", "media_url"])
            writer.writerows(out_tweets)

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

    def fetch(self, account, tweet_mode='extended', limit=500):
        # 3250 tweets is max for parsing from each user
        dir_name = account
        api = self.api
        self.fetch_user(account)
        epoch = 1
        video_urls = set()
        image_urls = set()
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
        os.mkdir(dir_name)
        for tweet in tweepy.Cursor(api.user_timeline, id=account, tweet_mode=tweet_mode).items(limit):
            id_tweet = tweet.id_str
            date_tweet = tweet.created_at
            text_tweet = tweet.full_text
            user_id = tweet.user.name
            tweet_location = tweet.user.location
            print("Tweets: {}".format(epoch))
            epoch += 1
            rv = self.process_tweet_media(tweet)
            for r in rv:
                if r.endswith("mp4"):
                    video_urls.add(r)
                else:
                    image_urls.add(r)
            self.out_tweets.append([user_id, id_tweet, date_tweet, text_tweet, tweet_location, rv])
            # save_all_to_db(self.out_tweets)
        self.save_data(video_urls, image_urls, self.out_tweets, account)


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
