from typing import List, Dict


categoryMatchKeywords: Dict[str, List[str]] = {
    'studying': ["assignment", "task"],
    'sports': ["sport", "football", "basketball", "sport opportunities", "team"],
    'social activities': ["social", "social activities", "student association", "events", "upcoming events", "upcoming social events", "social events"],
}

match_keywords = {
    "sports": {
        "aikido": ["aikido", "sport"],
        "basketball": ["basketball", "teamsport"],
        "tennis": ["tennis"],
        "swimming": ["swimming"],
        "football": ["football"],
        "zumba": ["zumba"],
        "karate": ["karate"],
        "yoga": ["yoga"],
        "waterpolo": ["waterpolo"],
    },
    "associations": {
        "Poetry Pals": ["art", "poetry"],
        "Debate Club": ["debate"],
        "Science Society": ["science"],
        "Painting and Pottery": ["arts", "art", "painting", "pottery"],
        "Language Club": ["language", "culture", "international"],
        "International Students Society": ["international", "erasmus"],
        "Students for Sustainability": ["sustainability", "environment"],
        "Animal Shelter Volunteers": ["animals", "help", "volounteering"],
        "Bunch of Backpackers": ["nature, backpackers", "backpacking", "travel", "travelling", "environment"]
    }
}


redundant_words: List[str] = ["we", "the", "and", "why", "what", "where", "who", "when", "how", "because", "if", "this", "that", "there", "than", "then", "however", "maybe", "some", "to", "from", "back", "more", "less", "better", "worse", "else", "please", "help", "do", "you", "many", "question", "questions", "we", "have", "any", "at", "our", "university", "i", "would", "love", "like", "to", "join", "a", "an"]
