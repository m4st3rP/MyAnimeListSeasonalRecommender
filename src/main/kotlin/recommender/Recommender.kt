package recommender

import okhttp3.OkHttpClient
import okhttp3.Request
import java.io.File
import java.io.FileOutputStream

// TODO anime: source
// TODO characters_staff: staff
class Recommender(private var username: String) {
    private var animeMap: MutableMap<Int, Int> = HashMap() // Key is ID of an anime and Value is the users score
    private var genreMap: MutableMap<Int, ArrayList<Int>> = HashMap()
    private var studioMap: MutableMap<Int, ArrayList<Int>> = HashMap()
    private var staffMap: MutableMap<String, ArrayList<Int>> = HashMap()
    private var sourceMaterialMap: MutableMap<String, ArrayList<Int>> = HashMap()
    private var typeMap: MutableMap<String, ArrayList<Int>> = HashMap()

    /**
     * This method downloads a users animelist and puts the anime ID and the users score into the animeMap.
     */
    fun analyzeAnimelistJSON() {
        var page = 1 // json is paged
        var lastPage = false

        while (!lastPage) {
            // download JSON
            downloadFile("https://api.jikan.moe/v3/user/$username/animelist/all/$page", "animelist.json") // page because the API only retrieves 300 anime per page

            // extract data from JSON
            val json = File("animelist.json")
            val jsonAsString = json.readText().substringAfter("\"anime\":[{\"") // delete the beginning before the animes
            val animes = jsonAsString.split("mal_id\":") // split between the animes

            // add every anime and their score to the map
            if (animes.size <= 1) { // 1 because we have the trash string at the beginning TODO change to 0 when we have a better solution
                lastPage = true
            } else {
                for (anime in animes) {
                    if (anime == "") { // for some reason we get an empty string at the beginning TODO create a better solution
                        continue
                    }
                    // extract score from string
                    val id = anime.substringBefore(',').toInt()
                    val score = anime.substringAfter("\"score\":").substringBefore(',').toInt()

                    if (score > 0) { // only add a score if there was actually one set (0 means no score)
                        animeMap[id] = score

                        // add type to typeMap
                        val type = anime.substringAfter("\"type\":\"").substringBefore('"')
                        if (!typeMap.containsKey(type)) {
                            typeMap[type] = ArrayList()
                        }
                        typeMap[type]?.add(score)
                    }
                }
                page++
            }
            // TODO remove
            /*for (a in animeMap.keys) {
                println(a)
            }
            for (a in typeMap.keys) {
                println("$a: ${typeMap[a]?.average()}")
            }*/
        }
    }

    fun analyzeAnimeMap() {
        val waitTimeSeconds: Long = 3
        animeMap[35240] = 5 // TODO remove later
        println("This process will take about ${animeMap.keys.size * waitTimeSeconds}")
        for (anime in animeMap.keys) {
            /*println("Processing anime: $anime")
            Thread.sleep(waitTimeSeconds * 1000)*/ // wait 3 seconds because the jikan API wants that (apparently that is not needed for cachec requests)
            val animeScore = animeMap[anime]
            if (animeScore == null) {
                continue
            }

            // download anime specific json
            downloadFile("https://api.jikan.moe/v3/anime/$anime", "anime.json")
            val json = File("anime.json")

            // extract studio info
            val jsonAsStringStudioData = json.readText().substringAfter("\"studios\":[{\"").substringBefore("\"genres\"")
            val studioInfo = jsonAsStringStudioData.split("mal_id\":")

            // add every studio to the map while calculating their score
            for (studio in studioInfo) {
                val studioID = studio.substringBefore(',')
                if (studioID == "") {
                    continue
                }
                val studioIDint = studioID.toInt()

                if (!studioMap.containsKey(studioIDint)) {
                    studioMap[studioIDint] = ArrayList()
                }
                studioMap[studioIDint]?.add(animeScore)
                //studioMap[studioIDint]?.add(animeScore) ?:  studioMap[studioIDint] = ArrayList<Int>()// TODO actually add stuff to the map

            }

            // extract genre info
            val jsonAsStringGenreData = json.readText().substringAfter("\"genres\":[{").substringBefore(",\"opening_themes\"")
            val genreInfo = jsonAsStringGenreData.split("mal_id\":")

            // add every genre to the map while calculating its score
            for (genre in genreInfo) {
                if (genre == "" || genre == "\"") {
                    continue
                }
                val genreIDint = genre.substringBefore(',').toInt()
                genreMap[genreIDint]?.add(animeScore) // TODO actually add stuff to the map
            }
        }
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