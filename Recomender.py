from collections import defaultdict
from jikanpy import Jikan
from EpisodesAmount import EpisodesAmount
import time


SLEEP_TIME = 4

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

        self.analyzed_anime_dic = {}

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
            if animelist["request_cached"] is False:
                time.sleep(SLEEP_TIME)
                print("sleep")
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
        print("Started gathering anime data")
        for animeID in self.anime_dic.keys():
            anime = self.jikan.anime(animeID)
            if anime["request_cached"] is False:
                time.sleep(SLEEP_TIME)
                print("sleep")
            anime_staff_full = self.jikan.anime(animeID, extension='characters_staff')
            anime_staff = anime_staff_full["staff"]
            if anime_staff_full["request_cached"] is False:
                time.sleep(SLEEP_TIME)
                print("sleep")
            score = self.anime_dic[animeID]

            for genre in anime["genres"]:
                self.genre_dic[genre["mal_id"]].append(score)

            for studio in anime["studios"]:
                self.studio_dic[studio["mal_id"]].append(score)

            self.source_material_dic[anime["source"]].append(score)
            self.type_dic[anime["type"]].append(score)

            episodes = anime["episodes"]
            if episodes > 0:
                episodes_enum = self.get_episode_amount_enum(episodes)
                self.episodes_amount_dic[episodes_enum].append(score)

            for staff_member in anime_staff:  # TODO filter after position or specific positions only
                self.staff_dic[staff_member["mal_id"]].append(score)

    def analyze_seasonal_anime(self, year, season):
        seasonal_anime_full = self.jikan.season(year=year, season=season)
        if seasonal_anime_full["request_cached"] is False:
            time.sleep(SLEEP_TIME)
            print("sleep")
        seasonal_anime = seasonal_anime_full["anime"]
        print("Started analyzing seasonal anime")
        for anime in seasonal_anime:
            anime_staff_full = self.jikan.anime(anime["mal_id"], extension='characters_staff')
            if anime_staff_full["request_cached"] is False:
                time.sleep(SLEEP_TIME)
                print("sleep")
            anime_staff = anime_staff_full["staff"]
            score = 0.0
            score_addition_counter = 0

            genre_amount = 0
            genre_score = 0.0
            for genre in anime["genres"]:
                if genre["mal_id"] in self.genre_dic.keys():
                    genre_amount += 1
                    genre_score += sum(self.genre_dic[genre["mal_id"]]) / len(self.genre_dic[genre["mal_id"]])
            if genre_amount > 0:
                score += genre_score / genre_amount
                score_addition_counter += 1

            studio_amount = 0
            studio_score = 0.0
            for studio in anime["producers"]:
                if studio["mal_id"] in self.studio_dic.keys():
                    studio_amount += 1
                    studio_score += sum(self.studio_dic[studio["mal_id"]]) / len(self.studio_dic[studio["mal_id"]])
            if studio_amount > 0:
                score += studio_score / studio_amount
                score_addition_counter += 1

            if anime["source"] in self.source_material_dic:
                source_score = sum(self.source_material_dic[anime["source"]]) / len(
                    self.source_material_dic[anime["source"]])
                if source_score > 0:
                    score += source_score
                    score_addition_counter += 1

            if anime["type"] in self.type_dic:
                type_score = sum(self.type_dic[anime["type"]]) / len(self.type_dic[anime["type"]])
                if type_score > 0:
                    score += type_score
                    score_addition_counter += 1

            episode_amount = anime["episodes"]
            if episode_amount is None:
                episode_amount = 0
            if episode_amount > 0:
                episode_enum = self.get_episode_amount_enum(episode_amount)
                if episode_enum in self.episodes_amount_dic:
                    episode_amount_score = sum(self.episodes_amount_dic[episode_enum]) / len(
                        self.episodes_amount_dic[episode_enum])
                    if episode_amount_score > 0:
                        score += episode_amount_score
                        score_addition_counter += 1

            staff_score = 0.0
            staff_amount = 0
            for staff_member in anime_staff:
                if staff_member["mal_id"] in self.staff_dic:
                    staff_amount += 1
                    staff_score += sum(self.staff_dic[staff_member["mal_id"]])/len(self.staff_dic[staff_member["mal_id"]])
            if staff_amount > 0:
                staff_score /= staff_amount
                score += staff_score
                score_addition_counter += 1

            if score_addition_counter > 0:
                self.analyzed_anime_dic[anime["mal_id"]] = score / score_addition_counter

    def write_analyzed_anime_to_file(self):
        with open("analyzed_anime.txt", "w") as text_file:
            for anime in self.analyzed_anime_dic.keys():
                text_file.write(str(anime) + "," + str(self.analyzed_anime_dic[anime]) + "\n")
        print("Done writing file!")

    @staticmethod
    def get_episode_amount_enum(amount):
        if amount < 1:
            return None
        elif amount == 1:
            return EpisodesAmount.One
        elif 2 <= amount <= 8:
            return EpisodesAmount.TwoEight
        elif 9 <= amount <= 19:
            return EpisodesAmount.NineNineteen
        elif 20 <= amount <= 30:
            return EpisodesAmount.TwentyThirty
        elif 31 <= amount <= 50:
            return EpisodesAmount.ThirtyoneFifty
        elif 51 <= amount <= 100:
            return EpisodesAmount.FiftyoneOnehundred
        else:
            return EpisodesAmount.OnehundredonePlus
