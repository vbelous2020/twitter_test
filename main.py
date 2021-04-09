from db_funcs import get_user_from_db, get_publ_from_db, con
from parser_func import TweetParser


if __name__ == '__main__':
    users = ["AvakovArsen", "NatGeo", "disneyplus", "starwars", "IGN", "netflix", "Ukraine", "APUkraine", "Warcraft",
             "Wowhead", "ChristieGolden"]
    users2 = ["AvakovArsen"]
    parser = TweetParser()
    for user in users2:
        parser.fetch(user)
    # get_user_from_db(con)
    # get_publ_from_db(con)
