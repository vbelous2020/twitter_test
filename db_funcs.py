import mysql.connector
from mysql.connector import Error
import csv


# DATABASE twitter_test


def create_connection(host_name, user_name, user_password, db_name):
    con = None
    try:
        con = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return con


def create_database(con, query):
    cursor = con.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_query(con, query):
    cursor = con.cursor()
    try:
        cursor.execute(query)
        con.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(con, query):
    cursor = con.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


def get_user_from_db(con):
    query = "select * from users"
    cursor = con.cursor()
    cursor.execute(query)
    try:
        records = cursor.fetchall()
        print("Total number of rows in table: ", cursor.rowcount)
        print("Printing each row:\n")
        for row in records:
            print("Id: ", row[0], )
            print("Name: ", row[1])
            print("Followers: ", row[2])
            print("Location: ", row[3])
            print("Registration date: ", row[4], "\n")
    except Error as e:
        print(f"The error '{e}' occurred")


def save_all_tweets(out_tweets, screen_name):
    # db
    cursor = con.cursor()
    try:
        cursor.execute(""" INSERT INTO tweets (pub_id, pub_date, pub_text, media_url)
                        VALUES (%s, %s, %s, %s)""", out_tweets)
        con.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
    # csv
    with open('%s_tweets.csv' % screen_name, 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "created_at", "text", "media_url"])
        writer.writerows(out_tweets)


def get_publ_from_db(con):
    query = "select * from tweets"
    cursor = con.cursor()
    cursor.execute(query)
    try:
        records = cursor.fetchall()
        print("Total number of rows in table: ", cursor.rowcount)
        print("Printing each row:\n")
        for row in records:
            print("Id: ", row[0], )
            print("tweet_id: ", row[1])
            print("Tweet Text: ", row[2])
            print("user_id: ", row[3])
            print("Tweet date: ", row[4])
            print("Media url: ", row[5], "\n")
    except Error as e:
        print(f"The error '{e}' occurred")


create_users_table = """
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT, 
  name TEXT NOT NULL,   
  followers INT,
  geo TEXT,
  registration_date DATETIME,
  PRIMARY KEY (id) 
) ENGINE = InnoDB
"""

create_publications_table = """
CREATE TABLE IF NOT EXISTS tweets (
  id INT AUTO_INCREMENT, 
  pub_id INT NOT NULL, 
  pub_text TEXT NOT NULL, 
  user_id INTEGER NOT NULL, 
  pub_date DATETIME,
  media_url TEXT,
  FOREIGN KEY fk_user_id (user_id) REFERENCES users(id), 
  PRIMARY KEY (id)
) ENGINE = InnoDB
"""

con = create_connection("localhost", "root", "firmamento10", "twitter_test")
execute_query(con, create_users_table)
execute_query(con, create_publications_table)

# execute_query(con, "DROP TABLE publications")
# execute_query(con, "DROP TABLE users")
