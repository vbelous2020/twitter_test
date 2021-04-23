import tweepy
import csv
from tweepy import OAuthHandler
from keys_and_details import consumer_key, consumer_secret
from db_funcs import save_tweet_data, save_user, con, get_user_last_tweet, get_user_from_db, get_publ_from_db


def save_data(out_tweets, account):
    # save to CSV
    with open('%s_tweets.csv' % account, 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["user", "id", "created_at", "text", "location", "media_urls"])
        writer.writerows(out_tweets)
    # save to DB from CSV
    save_tweet_data(account)


def process_tweet_media(tweet):
    try:
        extended = tweet.extended_entities
        rv = []
        if not extended:
            rv.append('No media')
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
        return 'No media'


class TweetParser(object):
    def __init__(self):
        self.user_data = []
        self.out_tweets = []
        self.video_urls = []
        self.image_urls = []
        self.api = None
        auth = OAuthHandler(consumer_key, consumer_secret)
        self.api = tweepy.API(auth, wait_on_rate_limit=True)
        # This will make the rest of the code wait until update of the rate limit

    def first_check(self, list_of_users):
        for user in list_of_users:
            self.fetch_user(user)
            self.first_fetch(user)
        get_user_from_db(con)
        get_publ_from_db(con)

    def update_check(self, list_of_users):
        for user in list_of_users:
            self.update_fetch(user)
        get_publ_from_db(con)

    def update_fetch(self, account):
        last_id = get_user_last_tweet(con, account)
        self.first_fetch(account, last_id)

    def fetch_user(self, account):
        api = self.api
        twitter_user = api.get_user(account)
        username = twitter_user.screen_name
        followers_count = twitter_user.followers_count
        location = twitter_user.location
        if location == '':
            location = 'No location data'
        registration_date = twitter_user.created_at
        user_data = ([username, followers_count, location, registration_date])
        self.user_data = user_data
        save_user(user_data)

    def first_fetch(self, account, last_id=None, tweet_mode='extended', limit=3250):
        api = self.api
        count = 1
        video_urls = list()
        image_urls = list()
        for tweet in tweepy.Cursor(api.user_timeline, id=account,
                                   since_id=last_id, tweet_mode=tweet_mode).items(limit):
            id_tweet = tweet.id_str
            date_tweet = tweet.created_at
            text_tweet = tweet.full_text
            user_id = account
            tweet_location = tweet.user.location

            if tweet_location == '':
                tweet_location = 'No location data'
            print('Tweets: {}'.format(count))
            count += 1
            media_urls = process_tweet_media(tweet)
            for url in media_urls:
                if url.endswith('mp4'):
                    video_urls.append(url)
                else:
                    image_urls.append(url)

            out_tweets = ([user_id, id_tweet, date_tweet, text_tweet, tweet_location, media_urls])
            self.out_tweets.append(out_tweets)
        save_data(self.out_tweets, account)
        self.video_urls = video_urls
        self.image_urls = image_urls
