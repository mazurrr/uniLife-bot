#  .----------------.  .-----------------. .----------------.  .----------------.  .----------------.  .----------------.  .----------------.
# | .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
# | | _____  _____ | || | ____  _____  | || |     _____    | || |              | || |   ______     | || |     ____     | || |  _________   | |
# | ||_   _||_   _|| || ||_   \|_   _| | || |    |_   _|   | || |              | || |  |_   _ \    | || |   .'    `.   | || | |  _   _  |  | |
# | |  | |    | |  | || |  |   \ | |   | || |      | |     | || |    ______    | || |    | |_) |   | || |  /  .--.  \  | || | |_/ | | \_|  | |
# | |  | '    ' |  | || |  | |\ \| |   | || |      | |     | || |   |______|   | || |    |  __'.   | || |  | |    | |  | || |     | |      | |
# | |   \ `--' /   | || | _| |_\   |_  | || |     _| |_    | || |              | || |   _| |__) |  | || |  \  `--'  /  | || |    _| |_     | |
# | |    `.__.'    | || ||_____|\____| | || |    |_____|   | || |              | || |  |_______/   | || |   `.____.'   | || |   |_____|    | |
# | |              | || |              | || |              | || |              | || |              | || |              | || |              | |
# | '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
#  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'


from typing import List, Dict
from assets import lang, keywords, config, utils
import csv
import difflib
from datetime import date


def format_quickfix(data: List[List[str]]) -> List[List[str]]:
    fixed_data: List[List[str]] = []
    for line in data:
        temp_list: List[str] = []
        for word in line:
            if word[0] == " ":
                temp_list.append(word[1:])
            else:
                temp_list.append(word)
        fixed_data.append(temp_list)
    return fixed_data


def event_format(event: str) -> List[str]:  # Christmas Dinner (18 Dec)
    def reformat_date(event_date: str) -> str:
        months: Dict[str, str] = {
            "Jan": "01",
            "Feb": "02",
            "March": "03",
            "April": "04",
            "May": "05",
            "Sep": "09",
            "Oct": "10",
            "Nov": "11",
            "Dec": "12"
        }
        if int(event_date.split()[0]) < 10:
            return f"2024-{months[event_date.split()[1]]}-0{event_date.split()[0]}"
        return f"2024-{months[event_date.split()[1]]}-{event_date.split()[0]}"

    formatted_event: List[str] = []
    for event_index in range(len(event)):
        if event[event_index] == "(":
            formatted_event.append(event[0:event_index - 1])
            formatted_event.append(reformat_date(event[event_index + 1:-1]))
    return formatted_event


def formatUserInput(user_input: str) -> str:
    blacklisted_signs: List[str] = config.USER_INPUT_BLACKLISTED_SIGNS

    for sign in blacklisted_signs:
        user_input = user_input.replace(sign, "")

    splitted_input: List[str] = user_input.split()
    working_input: List[str] = splitted_input.copy()
    output: str = ""

    for word in splitted_input:
        if word.lower() in keywords.redundant_words:
            working_input.remove(word)

    for word_index in range(len(working_input)):
        if word_index == len(working_input) - 1:
            output += f"{working_input[word_index]}"
        else:
            output += f"{working_input[word_index]} "
    return output


def defineCategory(user_input: str) -> str:
    if user_input == config.END_KEYWORD:
        return "stop conversation"
    best_score: float = 0
    best_score_category: str = ""
    for category in config.DEFINE_CATEGORY_CATEGORIES:
        for word in keywords.categoryMatchKeywords[category]:
            seq = difflib.SequenceMatcher(None, user_input.lower(), word.lower())
            if config.DEBUG:
                print(config.debug + lang.SIMILARITY_SCORE_DEBUG.format(user_input=user_input, word=word, calc=seq.ratio() * 100))
            if seq.ratio() * 100 > best_score:
                best_score = seq.ratio() * 100
                best_score_category = category

    if best_score > config.MIN_REQUIRED_SIMILARITY_SCORE:
        return best_score_category
    else:
        best_score_category = "not found"
        return best_score_category


def findBestMatch(user_input: str, category: str) -> None:
    user_input_splitted = user_input.split()
    all_scores: Dict[str, float] = {}
    final_suggestions: List[str] = []

    def calcMatchScore(user_input: List[str], category: str, target: str) -> None:
        all_words_scores: List[float] = []
        for word in user_input:
            word_score: float = 0
            for keyword in keywords.match_keywords[category][target]:
                seq = difflib.SequenceMatcher(None, word.lower(), keyword.lower())
                if config.DEBUG:
                    print(
                        f"{config.debug}[DEBUG] Similarity score ({word.lower()} / {keyword.lower()} -> {seq.ratio() * 100}")
                if seq.ratio() * 100 > word_score:
                    word_score = seq.ratio() * 100
            if word_score > config.MIN_REQ_SIM_SCORE_MATCH[category]:
                all_words_scores.append(word_score)
        match_score: float = 0
        for score in all_words_scores:
            match_score += score
        try:
            match_score = match_score / len(all_words_scores)
            all_scores[target] = match_score
        except:
            all_scores[target] = 0

    for item in keywords.match_keywords[category]:
        calcMatchScore(user_input_splitted, category, item)

    for item in all_scores.items():
        if item[1] > config.MIN_REQ_SIM_SCORE_FINAL_MATCH[category]:
            final_suggestions.append(item[0])
    if len(final_suggestions) > 0:
        print(f"{config.message}{category.capitalize()} we managed to find for you:")
        for suggestion in final_suggestions:
            print(
                f"{config.message}➫ {config.special}{suggestion}{config.message}")
        print(config.message + lang.FINAL_ADNOTAION)
    else:
        match category:
            case "associations":
                print(config.message + lang.ASSOCIATION_MATCH_NOT_FOUND)
            case "sports":
                print(config.message + lang.SPORT_MATCH_NOT_FOUND)


def upcomingEvents(events) -> None:
    current_date = date.today()
    new_events_list: List[List[int | any]] = []
    for event in events:
        event_date = event[1].split('-')
        difference = (date(int(event_date[0]), int(event_date[1]), int(event_date[2])) - current_date).days
        if difference > 0:
            new_events_list.append([event[0], difference, event[1]])
    new_events_list.sort(key=lambda x: x[1])
    print(f"Upcoming events:")
    for event in range(1, 4):
        if new_events_list[event][1] == 1:
            print(
                f"➫ {config.special}{new_events_list[event][0]} {config.message}will be held in {new_events_list[event][1]} day ({config.highlight}{new_events_list[event][2]}{config.message})")
        else:
            print(
                f"➫ {config.special}{new_events_list[event][0]} {config.message}will be held in {new_events_list[event][1]} days ({config.highlight}{new_events_list[event][2]}{config.message})")


input_data = open("assets/unilife.csv", "r")
formatted_data = format_quickfix(list(csv.reader(input_data, delimiter=",")))
input_data.close()

data_sports: List[str] = []
data_associations: List[str] = []
data_events: List[List[str]] = []

for line in formatted_data[1:]:
    data_sports.append(line[0])
    data_associations.append(line[1])
    data_events.append(event_format(line[2]))

print(utils.Color.YELLOW + utils.greeting_title)
conversation_status: bool = True
username: str = input(config.message + lang.REQUEST_NAME)
print(config.message + lang.GREETING.format(username=username))

while conversation_status:
    is_struggling_correct: bool = False
    want_to_share_correct: bool = False
    has_specific_sport_correct: bool = False
    user_activities_choice_correct: bool = False
    user_input: str = input(config.message + lang.CHOOSE_TOPIC)
    if config.DEBUG:
        print(config.debug + f"[DEBUG] Formatted user input: {formatUserInput(user_input)}")
    match defineCategory(formatUserInput(user_input)):
        case "studying":
            if config.DEBUG:
                print(config.debug + "[DEBUG] Category selected: Studying ")
            while not is_struggling_correct:
                is_struggling: str = input(config.message + lang.IS_STRUGGLING)
                if is_struggling.lower() == "yes":
                    is_struggling_correct = True
                    while not want_to_share_correct:
                        want_to_share: str = input(config.message + lang.WANT_TO_SHARE)
                        if want_to_share.lower() == "yes":
                            want_to_share_correct = True
                            print(config.message + lang.SUGGESTION_STUDY_GROUP)
                            print(config.message + lang.FINAL_ADNOTAION)
                        elif want_to_share.lower() == "no":
                            want_to_share_correct = True
                            print(config.message + lang.SUGGESTION_STUDENT_ADVISOR)
                            print(config.message + lang.FINAL_ADNOTAION)
                        else:
                            print(config.error + lang.YES_NO_INCORRECT_RESPONSE.format(
                                username=username))
                elif is_struggling.lower() == "no":
                    is_struggling_correct = True
                    print(config.message + lang.SUGGESTION_STUDENT_DESK)
                    print(config.message + lang.FINAL_ADNOTAION)
                else:
                    print(config.error + lang.YES_NO_INCORRECT_RESPONSE.format(
                        username=username))
            print(config.error + lang.END_CONVERSATION.format(end_keyword=config.END_KEYWORD))
        case "sports":
            if config.DEBUG:
                print(config.debug + "[DEBUG] Category selected: Sports")
            while not has_specific_sport_correct:
                has_specific_sport: str = input(config.message + lang.HAS_SPECIFIC_SPORT)
                if has_specific_sport.lower() == "yes":
                    has_specific_sport_correct = True
                    user_sport: str = input(config.message + lang.QUESTION_SPECIFIC_SPORT)
                    if user_sport.lower() in data_sports:
                        print(config.message + lang.SUGGESTION_SPORTS_CENTRE.format(sport=user_sport.capitalize()))
                        print(config.message + lang.FINAL_ADNOTAION)
                    else:
                        print(config.message + lang.SPORT_NOT_AVAILABLE)
                        for i in data_sports:
                            print(f"  -> {i}")
                        print(config.message + lang.FINAL_ADNOTAION)
                elif has_specific_sport.lower() == "no":
                    has_specific_sport_correct = True
                    sport_fit: str = input(config.message + lang.SPORT_FIT)
                    findBestMatch(formatUserInput(sport_fit), "sports")
                else:
                    print(config.message + lang.YES_NO_INCORRECT_RESPONSE.format(username=username))

            print(config.error + lang.END_CONVERSATION.format(end_keyword=config.END_KEYWORD))
        case "social activities":
            if config.DEBUG:
                print(config.debug + "[DEBUG] Category selected: Activities }")
            while not user_activities_choice_correct:
                user_activities_choice: str = input(config.message + lang.EVENTS_OR_ASSOCIATIONS)
                if user_activities_choice.lower() == "events":
                    user_activities_choice_correct = True
                    upcomingEvents(data_events)
                elif user_activities_choice.lower() == "associations":
                    user_activities_choice_correct = True
                    association_fit: str = input(config.message + lang.ASSOCIATION_FIT)
                    findBestMatch(formatUserInput(association_fit), "associations")
                else:
                    print(config.error + lang.EVENTS_OR_ASSOCIATIONS_ERROR.format(
                        username=username))

            print(config.error + lang.END_CONVERSATION.format(end_keyword=config.END_KEYWORD))
        case "not found":
            print(config.error + lang.CATEGORY_NOT_DEFINED.format(username=username))
            print(config.error + lang.END_CONVERSATION.format(end_keyword=config.END_KEYWORD))
        case "stop conversation":
            print(config.message + lang.END_MESSAGE.format(username=username))
            conversation_status = False
