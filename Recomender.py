from collections import defaultdict
from jikanpy import Jikan


class Recomender:
    def __init__(self, user_name):
        self.user_name = user_name
        self.jikan = Jikan()
        self.anime_dic = {}  # dic of anime id and it's score
        self.genre_dic = defaultdict(list)
        self.studio_dic = defaultdict(list)
        self.staff_dic = {}
        self.source_material_dic = {}
        self.type_dic = {}

    def gather_data(self):
        last_page = False
        page_num = 1

        while not last_page:
            animelist = self.jikan.user(username=self.user_name, request='animelist', page=page_num)
            for anime in animelist["anime"]:
                if anime["score"] > 0:
                    self.anime_dic[anime["mal_id"]] = anime["score"]
            if len(animelist) < 300:
                last_page = True
                print(len(self.anime_dic))
            page_num += 1

        for animeID in self.anime_dic.keys():
            anime = self.jikan.anime(animeID)

            for genre in anime["genres"]:
                self.genre_dic[genre["mal_id"]].append(self.anime_dic[animeID])

            for studio in anime["studios"]:
                self.studio_dic[studio["mal_id"]].append(self.anime_dic[animeID])
