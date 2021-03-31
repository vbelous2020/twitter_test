import tweepy
from twitter_secret_key import consumer_key, consumer_secret, access_key, access_secret
from db_funcs import con, get_user_from_db, get_publ_from_db, save_all_tweets
from mysql.connector import Error

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


def get_user(name, con):
    user = api.get_user(name)
    username = user.screen_name
    followers_count = user.followers_count
    location = user.location
    registration_date = user.created_at
    cursor = con.cursor()
    info = """INSERT INTO users (name, followers, geo, registration_date) VALUES (%s, %s, %s, %s)"""
    user_data = [username, followers_count, location, registration_date]
    try:
        cursor.execute(info, user_data)
        con.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def get_all_tweets(screen_name, con):
    all_tweets = []
    new_tweets = api.user_timeline(screen_name=screen_name, count=1)
    all_tweets.extend(new_tweets)
    oldest = all_tweets[-1].id - 1
    while len(new_tweets) > 0:
        print("getting tweets before %s" % oldest)
        # tweepy.Cursor(api.user_timeline, id=screen_name, max_id=oldest, tweet_mode='extended').items(200)
        new_tweets = api.user_timeline(screen_name=screen_name, count=200,
                                       max_id=oldest)
        all_tweets.extend(new_tweets)
        oldest = all_tweets[-1].id - 1
        print("...%s tweets downloaded so far" % (len(all_tweets)))
    out_tweets = []
    for tweet in all_tweets:
        id_tweet = tweet.id_str
        date_tweet = tweet.created_at
        text_tweet = tweet.text
        out_tweets.append([id_tweet, date_tweet, text_tweet])
        try:
            print(tweet.entities['media'][0]['media_url'])
        except (AttributeError, KeyError):
            pass
        else:
            media_url = tweet.entities['media'][0]['media_url']
            out_tweets.append([media_url])
    save_all_tweets(out_tweets, screen_name)


if __name__ == '__main__':
    # get_user("AvakovArsen", con)
    # get_user_from_db(con)
    get_all_tweets("AvakovArsen", con)
    get_publ_from_db(con)
