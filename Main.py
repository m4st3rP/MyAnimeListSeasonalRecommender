from collections import defaultdict
from jikanpy import Jikan

jikan = Jikan()

animeDic = {}  # dic of anime id and it's score
genreDic = defaultdict(list)
studioDic = defaultdict(list)
staffDic = {}
sourceMaterialDic = {}
typeDic = {}

user = "masterP"  # TODO replace with input


# TODO implement animelist paging
animelist = jikan.user(username=user, request='animelist')

for anime in animelist["anime"]:
    if anime["score"] > 0:
        animeDic[anime["mal_id"]] = anime["score"]

for animeID in animeDic.keys():
    anime = jikan.anime(animeID)

    for genre in anime["genres"]:
        genreDic[genre["mal_id"]].append(animeDic[animeID])

    for studio in anime["studios"]:
        studioDic[studio["mal_id"]].append(animeDic[animeID])
    print()