package recommender

fun main(args: Array<String>) {
    var input: String? = ""
    while (input == null) {
        println("Enter MAL username!")
        input = readLine()
    }
    val recommender = Recommender(input)

    recommender.analyzeAnimelistJSON()
}
