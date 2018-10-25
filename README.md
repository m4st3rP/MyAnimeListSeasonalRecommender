# MyAnimeListSeasonalRecommender

This is a program that analyzes what genres, studios and anime staff you liked on MyAnimeList and based upon that gives you season specific recommendations in a CSV-file (where the cells are seperated by ^), where the first column is the MAL ID and the second column is the score. The results are not really accurate since the algorithm is rather primitive.

It can also return the score of a specific anime by its ID and a CSV-file with your top staff members.

Uses this awesome API: https://jikan.docs.apiary.io/# and this also awesome Wrapper for the API: https://github.com/AWConant/jikanpy
