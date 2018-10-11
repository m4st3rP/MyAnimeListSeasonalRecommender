package recommender

import java.io.File

class Recommender(username: String) {
    var animeMap: MutableMap<Int, Double> = HashMap()
    var genreMap: MutableMap<String, Double> = HashMap()
    var studioMap: MutableMap<String, Double> = HashMap()
    var staffMap: MutableMap<String, Double> = HashMap()

    fun analyzeAnimelistJSON() {
        val json = File("animelist.json") // "https://api.jikan.moe/v3/user/$username/animelist"
        val jsonAsString = json.readText().substringAfter("\"anime\":[{\"") // delete the beginning before the animes
        val animes = jsonAsString.split("mal_id\":") // split between the animes
        for (anime in animes) {
            if (anime == "") { // for some reason we get an empty string at the beginning TODO create a better solution
                continue
            }
            val id = anime.substringBefore(',').toInt()
            val score = anime.substringAfter("\"score\":").substringBefore(',').toDouble()

            if (score > 0.0) {
                animeMap[id] = score
            }
        }

    }

    fun analyeAnimeMap() {

    }
}