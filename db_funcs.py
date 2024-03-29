import mysql.connector
import pandas as pd
from mysql.connector import Error
from keys_and_details import host_name, user_name, user_password, db_name

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
  user_id TEXT NOT NULL, 
  pub_id BIGINT NOT NULL, 
  pub_date TEXT NOT NULL,
  pub_text TEXT NOT NULL,
  pub_location TEXT, 
  media_url TEXT,
  PRIMARY KEY (id)
) ENGINE = InnoDB
"""


def create_connection(host, user, password, db):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            passwd=password,
            database=db
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


def save_user(user_data):
    cursor = con.cursor()
    info = """INSERT INTO users (name, followers, geo, registration_date) VALUES (%s, %s, %s, %s)"""
    try:
        cursor.execute(info, user_data)
        con.commit()
    except Error as e:
        print(f"The error '{e}' occurred")


def save_tweet_data(account):
    cursor = con.cursor()
    data = pd.read_csv(f'/Users/vladimirbelous/Desktop/Учеба/Work/twitter_test/{account}_tweets.csv')
    df = pd.DataFrame(data, columns=['user', 'id', 'created_at', 'text', 'location', 'media_urls'])
    try:
        for row in df.itertuples():
            cursor.execute("""INSERT INTO tweets (user_id, pub_id, pub_date, pub_text, 
                              pub_location, media_url)
                              VALUES (%s, %s, %s, %s, %s, %s)""",
                           (row.user, row.id, row.created_at, row.text, row.location, row.media_urls))
        con.commit()
    except Error as e:
        print(f"The error '{e}' occurred")


def get_user_from_db(connection):
    query = "select * from users"
    cursor = connection.cursor()
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


def get_publ_from_db(connection):
    query = "select * from tweets ORDER BY user_id, pub_date"
    cursor = connection.cursor()
    cursor.execute(query)
    try:
        records = cursor.fetchall()
        print("Total number of rows in table: ", cursor.rowcount)
        print("Printing each row: \n")
        for row in records:
            print("Record #", row[0])
            print("User id: ", row[1])
            print("Tweet id: ", row[2])
            print("Tweet date: ", row[3])
            print("Tweet Text: ", row[4])
            print("Location: ", row[5])
            print("Media url: ", row[6], "\n")
    except Error as e:
        print(f"The error '{e}' occurred")


def get_user_last_tweet(connection, account):
    query = "select * from tweets ORDER BY user_id, pub_date"
    cursor = connection.cursor()
    cursor.execute(query)
    try:
        records = cursor.fetchall()
        for row in records:
            if row[1] == account:
                tweet_id = str(row[2])
                return tweet_id
    except Error as e:
        print(f"The error '{e}' occurred")


def save_active_status(flag, tweet_id):
    cursor = con.cursor()
    info = """UPDATE Tweets SET Deleted=%s WHERE Tweet_Id=%s"""
    try:
        cursor.execute(info, (flag, tweet_id))
        con.commit()
    except Error as e:
        print(f"The error '{e}' occurred")


# Connection
con = create_connection(host_name, user_name, user_password, db_name)

# DB Creation
execute_query(con, create_users_table)
execute_query(con, create_publications_table)

# DB Drop
# execute_query(con, "DROP TABLE users")
# execute_query(con, "DROP TABLE tweets")
