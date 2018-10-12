package recommender

fun main(args: Array<String>) {
    var input: String? = "masterP" // TODO change back to blank String
    while (input == null) {
        println("Enter MAL username!")
        input = readLine() // TODO fix input
    }
    val recommender = Recommender(input)

    //recommender.analyzeAnimelistJSON()
    recommender.analyzeAnimeMap()
}
