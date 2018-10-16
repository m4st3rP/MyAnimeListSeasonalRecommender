from collections import defaultdict

from jikanpy import Jikan
import urllib.request

jikan = Jikan()

animeDic = {}  # dic of anime id and it's score
genreDic = defaultdict(list)
studioDic = defaultdict(list)
staffDic = {}
sourceMaterialDic = {}
typeDic = {}

user = "masterP"  # TODO replace with input

animeListLink = "https://api.jikan.moe/v3/user/" + user + "/animelist"
urllib.request.urlretrieve(animeListLink, "animelist.json")  # download file

# TODO implement animelist paging
with open("animelist.json", "r") as animelist:
    data = animelist.readlines()  # transform file to string
    splitData = data[0].split('{"mal_id":')  # create lists of substrings split at delimiter
    for sd in range(1, len(splitData) - 1):  # start at position 1 because the first string is not an anime
        sdd = splitData[sd].split(',')  # split after colon so the values stand alone
        animeID = int(sdd[0])  # id is 0st entry
        scoreSplit = sdd[7].split(":")  # score is 7th entry but needs to be further splitted
        score = int(scoreSplit[1])  # in this further split the score itself is at position 1
        if score > 0:  # add anime only if the score is set (0 means no score)
            animeDic[animeID] = score

useranimelist = jikan.user(username='masterP', request='animelist')

for animeID in animeDic.keys():
    anime = jikan.anime(animeID)

    for genre in anime["genres"]:
        genreDic[genre["mal_id"]].append(animeDic[animeID])

    for studio in anime["studios"]:
        studioDic[studio["mal_id"]].append(animeDic[animeID])
    print()