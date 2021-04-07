import json
import mysql.connector
from mysql.connector import Error

# import csv
# DATABASE twitter_test

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


def save_user_to_db(user_data):
    cursor = con.cursor()
    info = """INSERT INTO users (name, followers, geo, registration_date) VALUES (%s, %s, %s, %s)"""
    try:
        cursor.execute(info, user_data)
        con.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def save_all_to_db(out_tweets):
    cursor = con.cursor()
    info = """ INSERT INTO tweets (user_id, pub_id, pub_date, pub_text, pub_location, media_url)
                                VALUES (%s, %s, %s, %s, %s, %s)"""
    try:
        cursor.executemany(info, out_tweets)
        con.commit()
        print("Query executed successfully")
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
    query = "select * from tweets"
    cursor = connection.cursor()
    cursor.execute(query)
    try:
        records = cursor.fetchall()
        print("Total number of rows in table: ", cursor.rowcount)
        print("Printing each row: \n")
        for row in records:
            print("User id: ", row[0], )
            print("Tweet id: ", row[1])
            print("Tweet date: ", row[2])
            print("Tweet Text: ", row[3])
            print("Location: ", row[4])
            print("Media url: ", row[5], "\n")
    except Error as e:
        print(f"The error '{e}' occurred")


con = create_connection("localhost", "root", "firmamento10", "twitter_test")
execute_query(con, create_users_table)
execute_query(con, create_publications_table)
# execute_query(con, "DROP TABLE users")
# execute_query(con, "DROP TABLE tweets")

# get_user_from_db(con)
