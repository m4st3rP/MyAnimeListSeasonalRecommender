from Recomender import Recomender

"""
analyzes a season for a specific user and writes the result into a file and optionally also a file for the staff they like
write_staff_file = Boolean if the user also wants to get staff they like
"""
def analyze_season(write_staff_file):
    """
    year = int(input("Enter the season year: "))
    season = str(input("Enter the season (winter, spring, summer or fall): "))
    kids = str(input("Enter yes or no if you want kids shows: "))
    if kids.lower() is "yes":
        kids_boolean = True
        print("You selected yes.")
    else:
        kids_boolean = False
        print("You selected no.")
    r18 = str(input("Enter yes or no if you want R18 (Hentai) shows: "))
    if r18.lower() is "yes":
        r18_boolean = True
        print("You selected yes.")
    else:
        r18_boolean = False
        print("You selected no.")
    """

    username = "masterP"
    year = 2019
    season = "winter"
    kids_boolean = False
    r18_boolean = False
    recomender = Recomender(username)
    recomender.fill_anime_dic()
    recomender.gather_anime_data_from_anime_dic()
    recomender.analyze_seasonal_anime(year, season, kids_boolean, r18_boolean)
    recomender.write_analyzed_anime_to_file()
    if write_staff_file:
        recomender.write_analyzed_staff_to_file()


"""
analyzes a single anime with its MAL id
"""
def analyze_one_anime():
    mal_id = int(input("Enter the MAL id of the anime: "))
    recomender = Recomender(username)
    recomender.fill_anime_dic()
    recomender.gather_anime_data_from_anime_dic()
    recomender.analyze_anime(mal_id)
    recomender.write_analyzed_anime_to_file()


"""
writes a csv file for the staff a specific user likes
"""
def analyze_staff():
    recomender = Recomender(username)
    recomender.fill_anime_dic()
    recomender.gather_anime_data_from_anime_dic()
    recomender.write_analyzed_staff_to_file()


#username = str(input("Enter your MAL username: "))
#mode = str(input("Enter \"season\" if you want to analyze a season or \"staff\" if you want to analyze which staff you like or \"both\" for both or \"single\" for one anime: "))
mode = "season"

if mode.lower() == "season" or mode.lower() == "\"season\"":
    print("You selected \"season\".")
    analyze_season(False)
elif mode.lower() == "staff" or mode.lower() == "\"staff\"":
    print("You selected \"staff\".")
    analyze_staff()
elif mode.lower() == "both" or mode.lower() == "\"both\"":
    print("You selected \"both\".")
    analyze_season(True)
elif mode.lower() == "single" or mode.lower() == "\"single\"":
    print("You selected \"single\".")
    analyze_one_anime()
else:
    print("You selected neither.")
