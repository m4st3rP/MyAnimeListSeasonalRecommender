package recommender

import okhttp3.OkHttpClient
import okhttp3.Request
import java.io.File
import java.io.FileOutputStream

class Recommender(private var username: String) {
    private var animeMap: MutableMap<Int, Double> = HashMap() // Key is ID of an anime and Value is the users score
    private var genreMap: MutableMap<String, Double> = HashMap()
    private var studioMap: MutableMap<String, Double> = HashMap()
    private var staffMap: MutableMap<String, Double> = HashMap()

    /**
     * This method downloads a users animelist and puts the anime ID and the users score into the animeMap.
     */
    fun analyzeAnimelistJSON() {
        // download JSON
        downloadFile("https://api.jikan.moe/v3/user/$username/animelist", "animelist.json")

        // extract data from JSON
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
                //println("$id: $score")
            }
        }
    }

    fun analyzeAnimeMap() {

    }

    private fun downloadFile(url: String, name: String) {
        val client = OkHttpClient()
        val request = Request.Builder().url(url).build()
        val response = client.newCall(request).execute()
        /*if (!response.isSuccessful()) {
            throw IOException("Failed to download file: " + response)
        }*/
        val fos = FileOutputStream(name)
        fos.write(response.body()?.bytes())
        fos.close()
    }
}