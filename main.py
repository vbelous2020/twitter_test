from parser_func import TweetParser


if __name__ == '__main__':
    users = ["AvakovArsen", "NatGeo", "disneyplus", "starwars", "IGN", "netflix", "Ukraine", "APUkraine", "Warcraft",
             "Wowhead", "ChristieGolden"]
    users2 = ["Volodym27613062"]
    parser = TweetParser()
    # For the First Check
    parser.first_check(users2)

    # Update for getting new tweets
    parser.update_fetch(users2)
