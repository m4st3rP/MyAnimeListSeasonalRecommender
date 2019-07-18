from collections import defaultdict

from jikanpy import Jikan
from EpisodesAmount import EpisodesAmount
import time

SLEEP_TIME = 3.0  # seconds to wait after a non cached request
# importance factors of attributes of anime
GENRE_FACTOR = 1
STUDIO_FACTOR = 1
SOURCE_MATERIAL_FACTOR = 0.3
TYPE_FACTOR = 0.25
EPISODE_AMOUNT_FACTOR = 0.20
STAFF_FACTOR = 1.5
POSITION_SET = {"Producer", "Chief Producer", "Assistant Director", "Series Composition", "Screenplay", "Script",
                "Setting", "Production Assistant", "Co-Producer", "Original Creator", "Co-Director", "Director",
                "Assistant Producer", "Creator", "Series Production Director", "Planning Producer", "Planning",
                "Storyboard"}  # A set of staff position that will be not filtered out

"""
A class that analyzes a MAL user and can analyze how well they will like the anime of a season or what staff they like
"""
class Recomender:
    def __init__(self, user_name):
        self.user_name: str = user_name  # MAL username
        self.jikan = Jikan()  # API object

        self.anime_dic = {}  # dic of anime id and it's score
        self.genre_dic = defaultdict(list)  # dic of genres and a list of user scores for them
        self.studio_dic = defaultdict(list)  # dic of studios and a list of user scores for them
        self.source_material_dic = defaultdict(list)  # dic of source materials and a list of user scores for them
        self.type_dic = defaultdict(list)  # dic of types and a list of user scores for them
        self.episodes_amount_dic = defaultdict(list)  # dic of episode amount enums and a list of user scores for them
        self.staff_dic = defaultdict(list)  # dic of staff people and a list of user scores for them

        self.analyzed_anime_dic = {}  # dic of analyzed seasonal anime and their scores
        self.anime_name_dic = {}  # dic of MAL anime ids and names
        self.staff_name_dic = {}  # dic of MAL staff ids and names

    """
    Fills the anime_dic with the users rated anime
    """
    def fill_anime_dic(self):
        print("Started filling anime dic.")
        last_page: bool = False
        page_num: int = 1

        while not last_page:  # the API only returns 300 anime so we may need to request multiple pages
            animelist = self.jikan.user(username=self.user_name, request='animelist', argument="all", page=page_num)
            if animelist["request_cached"] is False:
                time.sleep(SLEEP_TIME)  # if the request was uncached we need to add a delay or we get a 429
            for anime in animelist["anime"]:
                if anime["score"] > 0:  # only add the anime if the user set a score
                    self.anime_dic[anime["mal_id"]] = anime["score"]
            if len(animelist["anime"]) < 300:  # each page contains max 300 anime
                last_page = True
            page_num += 1

    """
    Gathers data like genre or studio scores based upon the anime in the anime dic
    """
    def gather_anime_data_from_anime_dic(self):
        print("Started gathering anime data from anime dic.")
        progress_counter = 1
        for animeID in self.anime_dic.keys():  # go though every anime
            if progress_counter % 10 == 1:
                print("Gathered " + str(progress_counter) + " anime.")
            progress_counter += 1

            anime = self.jikan.anime(animeID)
            if anime["request_cached"] is False:
                time.sleep(SLEEP_TIME)  # sleep to prevent 429
            anime_staff_full = self.jikan.anime(animeID, extension='characters_staff')  # get staff data
            anime_staff = anime_staff_full["staff"]
            if anime_staff_full["request_cached"] is False:
                time.sleep(SLEEP_TIME)
            score = self.anime_dic[animeID]

            for genre in anime["genres"]:  # add score for every genre
                self.genre_dic[genre["mal_id"]].append(score)

            for studio in anime["studios"]:  # add score for every studio
                self.studio_dic[studio["mal_id"]].append(score)

            self.source_material_dic[anime["source"]].append(score)  # add score for source material
            self.type_dic[anime["type"]].append(score)  # add score for type

            episodes = anime["episodes"]
            if episodes is None:  # if episodes are unset set the to zero
                episodes = 0
            if episodes > 0:  # only add score if episodes are set
                episodes_enum = self.get_episode_amount_enum(episodes)
                self.episodes_amount_dic[episodes_enum].append(score)

            for staff_member in anime_staff:
                for position in staff_member["positions"]:
                    #  only add the staff member if their position is relevant according to my own decision
                    if position in POSITION_SET:
                        self.staff_dic[staff_member["mal_id"]].append(score)
                        self.staff_name_dic[staff_member["mal_id"]] = staff_member["name"]

    """
    analyzes the anime of a specific season with the data gathered from the user
    year = int, year of the season
    season = string, season of the year (either winter, spring, summer or fall)
    kids = boolean, if you want to analyze kids shows
    r18 = if you want to analyze r18 (hentai) shows
    """
    def analyze_seasonal_anime(self, year, season, kids, r18):
        seasonal_anime_full = self.jikan.season(year=year, season=season)
        if seasonal_anime_full["request_cached"] is False:
            time.sleep(SLEEP_TIME)
        seasonal_anime = seasonal_anime_full["anime"]
        print("Started analyzing seasonal anime.")
        progress_counter = 1
        for anime in seasonal_anime:
            if progress_counter % 10 == 1:
                print("Analyzed " + str(progress_counter) + " anime.")
            progress_counter += 1

            if anime["continuing"]:  # if the anime is actually from a previous season, don't analyze it
                continue
            if not r18 and anime["r18"]:
                continue
            if not kids and anime["kids"]:
                continue
            self.analyze_anime(anime)

    """
    analyzes an anime and puts it and the score to the analyzed anime dic
    anime = either an anime object or the MAL ID as an int
    """
    def analyze_anime(self, anime):
        if isinstance(anime, int):  # if anime is an int get the anime object of it
            anime = self.jikan.anime(anime)

        score_divisor = 0  # variable through which the score in the end will be divided so that we get one that goes from 1 to 10 by adding the FACTOR of a value

        anime_staff_full = self.jikan.anime(anime["mal_id"], extension='characters_staff')
        if anime_staff_full["request_cached"] is False:
            time.sleep(SLEEP_TIME)
        anime_staff = anime_staff_full["staff"]
        score = 0.0
        score_addition_counter = 0  # count how many scores were actually added to the score

        genre_amount = 0
        genre_score = 0.0
        for genre in anime["genres"]:
            if genre["mal_id"] in self.genre_dic.keys():
                genre_amount += 1
                # get the average of the scores in the list
                genre_score += sum(self.genre_dic[genre["mal_id"]]) / len(self.genre_dic[genre["mal_id"]])
        if genre_amount > 0:  # only add if there was atleast one genre
            score += genre_score / genre_amount * GENRE_FACTOR
            score_addition_counter += 1
            score_divisor += GENRE_FACTOR

        studio_amount = 0
        studio_score = 0.0
        for studio in anime["producers"]:
            if studio["mal_id"] in self.studio_dic.keys():
                studio_amount += 1
                studio_score += sum(self.studio_dic[studio["mal_id"]]) / len(self.studio_dic[studio["mal_id"]])
        if studio_amount > 0:
            score += studio_score / studio_amount * STUDIO_FACTOR
            score_addition_counter += 1
            score_divisor += STUDIO_FACTOR

        if anime["source"] in self.source_material_dic:
            source_score = sum(self.source_material_dic[anime["source"]]) / len(
                self.source_material_dic[anime["source"]])
            if source_score > 0:
                score += source_score * SOURCE_MATERIAL_FACTOR
                score_addition_counter += 1
                score_divisor += SOURCE_MATERIAL_FACTOR

        if anime["type"] in self.type_dic:
            type_score = sum(self.type_dic[anime["type"]]) / len(self.type_dic[anime["type"]])
            if type_score > 0:
                score += type_score * TYPE_FACTOR
                score_addition_counter += 1
                score_divisor += TYPE_FACTOR

        episode_amount = anime["episodes"]
        if episode_amount is None:  # check if episodes are set and if they are not set them to 0
            episode_amount = 0
        if episode_amount > 0:
            episode_enum = self.get_episode_amount_enum(episode_amount)
            if episode_enum in self.episodes_amount_dic:
                episode_amount_score = sum(self.episodes_amount_dic[episode_enum]) / len(self.episodes_amount_dic[episode_enum])
                if episode_amount_score > 0:
                    score += episode_amount_score * EPISODE_AMOUNT_FACTOR
                    score_addition_counter += 1
                    score_divisor += EPISODE_AMOUNT_FACTOR

        staff_score = 0.0
        staff_amount = 0
        for staff_member in anime_staff:
            if staff_member["mal_id"] in self.staff_dic:
                staff_amount += 1
                staff_score += sum(self.staff_dic[staff_member["mal_id"]]) / len(self.staff_dic[staff_member["mal_id"]])
        if staff_amount > 0:
            staff_score /= staff_amount
            score += staff_score * STAFF_FACTOR
            score_addition_counter += 1
            score_divisor += STAFF_FACTOR

        if score_addition_counter > 0:
            self.anime_name_dic[anime["mal_id"]] = anime["title"]
            self.analyzed_anime_dic[anime["mal_id"]] = ((score / score_addition_counter) * (0.4 + 0.1 * score_addition_counter)) / (score_divisor / score_addition_counter)  # calculate the score and add the anime to the dic

    """
    writes a comma seperated value file with the result of the analyzed seasonal anime
    """
    def write_analyzed_anime_to_file(self):
        with open("analyzed_anime.txt", mode="w", encoding="utf8") as text_file:
            text_file.write("Name^MAL ID^Score\n")
            for anime in self.analyzed_anime_dic.keys():
                text_file.write(str(self.anime_name_dic[anime]) + "^" + str(anime) + "^" + str(self.analyzed_anime_dic[anime]) + "\n")
        print("Done writing anime file!")

    """
    writes a comma seperated value file with staff members and their score
    """
    def write_analyzed_staff_to_file(self):
        with open("analyzed_staff.txt", mode="w", encoding="utf8") as text_file:
            text_file.write("Name^MAL ID^Average^Amount^Score\n")

            max_len = -1
            for staff in self.staff_dic.keys():
                if len(self.staff_dic[staff]) > max_len:
                    max_len = len(self.staff_dic[staff])

            for staff in self.staff_dic.keys():
                FACTOR = 0.866
                length = len(self.staff_dic[staff])
                scores_list = self.staff_dic[staff]
                average = sum(scores_list) / length
                text_file.write(str(self.staff_name_dic[staff]) + "^" + str(staff) + "^" + str(average) + "^" + str(length) + "^" + str(average * FACTOR + ((length / max_len) * (1.0 - FACTOR) * 10.0)) + "\n")
        print("Done writing staff file!")

    """
    A Function that returns an Enum for summarizing episode amounts
    """
    @staticmethod
    def get_episode_amount_enum(amount) -> EpisodesAmount:
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
