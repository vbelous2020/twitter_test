import tweepy
from twitter_secret_key import consumer_key, consumer_secret, access_key, access_secret
from db_funcs import con, get_user_from_db, get_publ_from_db, save_all_tweets
from mysql.connector import Error
import time

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


def get_user(name, con):
    t_user = api.get_user(name)
    username = t_user.screen_name
    followers_count = t_user.followers_count
    location = t_user.location
    registration_date = t_user.created_at
    cursor = con.cursor()
    info = """INSERT INTO users (name, followers, geo, registration_date) VALUES (%s, %s, %s, %s)"""
    user_data = [username, followers_count, location, registration_date]
    try:
        cursor.execute(info, user_data)
        con.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def get_all_tweets(screen_name):
    all_tweets = []
    new_tweets = api.user_timeline(screen_name=screen_name, count=1)
    all_tweets.extend(new_tweets)
    oldest = all_tweets[-1].id - 1
    while len(new_tweets) > 0:
        print("getting tweets before %s" % oldest)
        new_tweets = api.user_timeline(screen_name=screen_name, count=200,
                                       max_id=oldest)
        all_tweets.extend(new_tweets)
        oldest = all_tweets[-1].id - 1
        print("...%s tweets downloaded so far" % (len(all_tweets)))
    out_tweets = []
    out_tweets_no_media = []
    for tweet in all_tweets:
        id_tweet = tweet.id_str
        date_tweet = tweet.created_at
        text_tweet = tweet.text
        user_id = tweet.user.name
        try:
            print(tweet.entities['media'][0]['media_url_https'])
        except KeyError:
            out_tweets_no_media.append([id_tweet, date_tweet, text_tweet, user_id])
        else:
            media_url = tweet.entities['media'][0]['media_url_https']
            out_tweets.append([id_tweet, date_tweet, text_tweet, media_url, user_id])
    save_all_tweets(out_tweets, screen_name, 'Media')
    save_all_tweets(out_tweets_no_media, screen_name, 'No media')


if __name__ == '__main__':
    list_of_users = ["AvakovArsen", "NatGeo", "disneyplus", "starwars", "IGN", "netflix", "Ukraine",
                     "APUkraine", "Warcraft", "Wowhead", "ChristieGolden"]
    # for user in list_of_users:
    #     get_user(user, con)
    #
    # get_user_from_db(con)
    # for user in list_of_users:
    #     get_all_tweets(user)
    #     time.sleep(5)
    get_publ_from_db(con)


# tweepy.Cursor(api.user_timeline, id=screen_name, max_id=oldest, tweet_mode='extended').items(200)
# try:
#     if 'entities' in tweet:
#         print(tweet.entities['media'][0]['media_url_https'])
#         media_url = tweet.entities['media'][0]['media_url']
#         out_tweets.append([media_url])
#     elif '' in tweet:
#         print(tweet.extended_entities["media"][0]["video_info"]["variants"][0]["url"])
#         media_url = tweet.extended_entities["media"][0]["video_info"]["variants"][0]["url"]
#         out_tweets.append([media_url])
#     else:
#         media_url = "No media"
#         out_tweets.append([media_url])
# except (AttributeError, KeyError, TypeError):
#     pass

