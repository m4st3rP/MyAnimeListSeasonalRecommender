from Recomender import Recomender

recomender = Recomender("masterP")
recomender.fill_anime_dic()
recomender.gather_anime_data()
recomender.analyze_seasonal_anime(2018, "fall")
recomender.write_analyzed_anime_to_file()