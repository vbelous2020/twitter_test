import tweepy
import csv
from twitter_secret_key import consumer_key, consumer_secret, access_key, access_secret
from create_table import con, get_user_from_db, get_publ_from_db
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
    try:
        cursor.execute("""
    INSERT INTO
      users (name, followers, geo, registration_date)
    VALUES
      (%s, %s, %s, %s)
    """, (username, followers_count, location, registration_date))
        con.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def get_all_tweets(screen_name, con):
    global date_tweet, id, text_tweet, media_url
    all_tweets = []
    new_tweets = api.user_timeline(screen_name=screen_name, count=1)
    all_tweets.extend(new_tweets)
    oldest = all_tweets[-1].id - 1
    while len(new_tweets) > 0:
        print("getting tweets before %s" % oldest)
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)
        all_tweets.extend(new_tweets)
        oldest = all_tweets[-1].id - 1
        print("...%s tweets downloaded so far" % (len(all_tweets)))

    out_tweets = []
    for tweet in all_tweets:
        id = tweet.id_str
        date_tweet = tweet.created_at
        text_tweet = tweet.text
        out_tweets.append([id, date_tweet, text_tweet])
        try:
            print(tweet.extended_entities.media_url)
        except AttributeError:
            pass
        else:
            media_url = tweet.entities.media.media_url
            out_tweets.append([media_url])
            cursor = con.cursor()
            try:
                cursor.execute("""
                    INSERT INTO
                      tweets (pub_id, pub_date, pub_text, media_url)
                    VALUES
                      (%s, %s, %s, %s)
                    """, (id, date_tweet, text_tweet, media_url))
                con.commit()
                print("Query executed successfully")
            except Error as e:
                print(f"The error '{e}' occurred")

    # csv
    with open('%s_tweets.csv' % screen_name, 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "created_at", "text", "media_url"])
        writer.writerows(out_tweets)


if __name__ == '__main__':

    # get_user("AvakovArsen", con)

    # get_user_from_db(con)

    get_all_tweets("AvakovArsen", con)

    get_publ_from_db(con)
