from collections import defaultdict
from jikanpy import Jikan
from EpisodesAmount import EpisodesAmount


class Recomender:
    def __init__(self, user_name):
        self.user_name = user_name
        self.jikan = Jikan()
        self.anime_dic = {}  # dic of anime id and it's score
        self.genre_dic = defaultdict(list)
        self.studio_dic = defaultdict(list)
        self.source_material_dic = defaultdict(list)
        self.type_dic = defaultdict(list)
        self.episodes_amount_dic = defaultdict(list)
        self.staff_dic = defaultdict(list)

    def test(self):
        animelist = self.jikan.user(username='masterP', request='animelist', argument='completed', page=2)
        animelist2 = self.jikan.user(username='masterP', request='animelist', argument='all', page=3)
        animelist3 = self.jikan.user(username='masterP', request='animelist', page=4)
        print()

    def fill_anime_dic(self):
        last_page = False
        page_num = 1

        while not last_page:
            animelist = self.jikan.user(username=self.user_name, request='animelist', page=page_num)
            for anime in animelist["anime"]:
                if anime["score"] > 0:
                    self.anime_dic[anime["mal_id"]] = anime["score"]
            if len(animelist["anime"]) < 300:
                last_page = True
                print(len(self.anime_dic))
            page_num += 1
            last_page = True  # TODO remove when Paging is fixed in jikanpy
            print(page_num)
        print(len(self.anime_dic))

    def gather_anime_data(self):
        for animeID in self.anime_dic.keys():
            anime = self.jikan.anime(animeID)
            anime_staff = self.jikan.anime(animeID, extension='characters_staff')["staff"]
            score = self.anime_dic[animeID]

            for genre in anime["genres"]:
                self.genre_dic[genre["mal_id"]].append(score)

            for studio in anime["studios"]:
                self.studio_dic[studio["mal_id"]].append(score)

            self.source_material_dic[anime["source"]].append(score)
            self.type_dic[anime["type"]].append(score)

            episodes = anime["episodes"]
            if episodes > 0:
                if episodes == 1:
                    episodes_enum = EpisodesAmount.One
                elif 2 <= episodes <= 8:
                    episodes_enum = EpisodesAmount.TwoEight
                elif 9 <= episodes <= 19:
                    episodes_enum = EpisodesAmount.NineNineteen
                elif 20 <= episodes <= 30:
                    episodes_enum = EpisodesAmount.TwentyThirty
                elif 31 <= episodes <= 50:
                    episodes_enum = EpisodesAmount.ThirtyoneFifty
                elif 51 <= episodes <= 100:
                    episodes_enum = EpisodesAmount.FiftyoneOnehundred
                else:
                    episodes_enum = EpisodesAmount.OnehundredPlus
                self.episodes_amount_dic[episodes_enum].append(score)

            for staff_member in anime_staff:  # TODO filter after position or specific positions only
                self.staff_dic[staff_member["mal_id"]].append(score)
