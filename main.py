from db_funcs import get_publ_from_db, con
from parser_func import TweetParser


if __name__ == '__main__':
    users = ["AvakovArsen", "NatGeo", "starwars", "IGN", "netflix", "Ukraine", "APUkraine"]
    # "Warcraft", "Wowhead", "ChristieGolden", "disneyplus"

    users2 = ["AvakovArsen"]        # one user for fast test
    parser = TweetParser()

    # For the First Check
    parser.first_check(users2)
    get_publ_from_db(con)

    # Update for getting new tweets
    # parser.update_fetch(users2)
