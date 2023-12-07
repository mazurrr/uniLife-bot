from typing import List, Dict

keywords_studying: List[str] = ["assignment", "task"]
keywords_sport: List[str] = ["sport", "football", "basketball", "sport opportunities", "team"]
keywords_social_activities: List[str] = ["social", "social activities", "student association", "events",
                                         "upcoming events", "upcoming social events", "social events"]
sport_keywords: Dict[str, List[str]] = {
    "aikido": [],
    "basketball": [],
    "tennis": [],
    "swimming": [],
    "football": [],
    "zumba": [],
    "karate": [],
    "yoga": [],
    "waterpolo": []
}
association_keywords: Dict[str, List[str]] = {
    "Poetry Pals": ["lorem ipsum"],
    "Debate Club": ["lorem ipsum"],
    "Science Society": ["lorem ipsum"],
    "Painting and Pottery": ["lorem ipsum"],
    "Language Club": ["lorem ipsum"],
    "International Students Society": ["lorem ipsum"],
    "Students for Sustainability": ["lorem ipsum"],
    "Animal Shelter Volunteers": ["animals", "help", "volounteering"],
    "Bunch of Backpackers": ["lorem ipsum"]
}

redundant_words: List[str] = ["we", "the", "and", "why", "what", "where", "who", "when", "how", "because", "if", "this", "that", "there", "than", "then", "however", "maybe", "some", "to", "from", "back", "more", "less", "better", "worse", "else", "please", "help", "do", "you", "many", "question", "questions", "we", "have", "any", "at", "our", "university"]
