from Recomender import Recomender

username = str(input("Enter your MAL username: "))
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

recomender = Recomender(username)
recomender.fill_anime_dic()
recomender.gather_anime_data()
recomender.analyze_seasonal_anime(year, season, kids_boolean, r18_boolean)
recomender.write_analyzed_anime_to_file()
