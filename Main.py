from Recomender import Recomender

username = str(input("Enter your MAL username: "))
year = int(input("Enter the season year: "))
season = str(input("Enter the season (winter, spring, summer or fall): "))
kids = str(input("Enter yes or no if you want kids shows: "))
r18 = str(input("Enter yes or no if you want R18 (Hentai) shows: "))

if kids.lower() is "yes":
    kids_boolean = True
else:
    kids_boolean = False

if r18.lower() is "yes":
    r18_boolean = True
else:
    r18_boolean = False

recomender = Recomender(username)
recomender.fill_anime_dic()
recomender.gather_anime_data()
recomender.analyze_seasonal_anime(year, season, kids_boolean, r18_boolean)
recomender.write_analyzed_anime_to_file()
