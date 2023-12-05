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
    for i in data:
        temp_list: List[str] = []
        for j in i:
            if j[0] == " ":
                temp_list.append(j[1:])
            else:
                temp_list.append(j)
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


def defineCategory(user_input: str) -> str:
    if user_input == config.END_KEYWORD:
        return "stop conversation"
    best_score: float = 0
    best_score_category: str = ""
    for word in keywords.keywords_sport:
        seq = difflib.SequenceMatcher(None, user_input.lower(), word.lower())
        if config.DEBUG:
            print(f"{config.bot_debug_format}[DEBUG] Similarity score ({user_input} / {word} -> {seq.ratio() * 100}")
        if seq.ratio() * 100 > best_score:
            best_score = seq.ratio() * 100
            best_score_category = "sports"
    for word in keywords.keywords_studying:
        seq = difflib.SequenceMatcher(None, user_input.lower(), word.lower())
        if config.DEBUG:
            print(f"{config.bot_debug_format}[DEBUG] Similarity score ({user_input} / {word} -> {seq.ratio() * 100}")
        if seq.ratio() * 100 > best_score:
            best_score = seq.ratio() * 100
            best_score_category = "studying"
    for word in keywords.keywords_social_activities:
        seq = difflib.SequenceMatcher(None, user_input.lower(), word.lower())
        if config.DEBUG:
            print(f"{config.bot_debug_format}[DEBUG] Similarity score ({user_input} / {word} -> {seq.ratio() * 100}")
        if seq.ratio() * 100 > best_score:
            best_score = seq.ratio() * 100
            best_score_category = "social activities"
    if best_score > config.MIN_REQUIRED_SIMILARITY_SCORE:
        return best_score_category
    else:
        best_score_category = "not found"
        return best_score_category


def findAssociation(user_input: str) -> None:  # TODO
    return None


def findSport(user_input: str) -> None: # TODO
    return None


def upcomingEvents(events) -> None:
    current_date = date.today()
    new_events_list: List[List[str, int]] = []
    for event in events:
        event_date = event[1].split('-')
        difference = (date(int(event_date[0]), int(event_date[1]), int(event_date[2])) - current_date).days
        if difference > 0:
            new_events_list.append([event[0], difference])
    new_events_list.sort(key=lambda x: x[1])
    print(f"Upcoming events:")
    for event in range(1, 4):
        if new_events_list[event][1] == 1:
            print(f"➫ {config.bot_message_special_format}{new_events_list[event][0]} {config.bot_message_format}will be held in {new_events_list[event][1]} day")
        else:
            print(f"➫ {config.bot_message_special_format}{new_events_list[event][0]} {config.bot_message_format}will be held in {new_events_list[event][1]} days")
    return None


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
username: str = input(config.bot_message_format + lang.REQUEST_NAME)
print(config.bot_message_format + lang.GREETING.format(username=username))
while conversation_status:
    is_struggling_correct: bool = False
    want_to_share_correct: bool = False
    has_specific_sport_correct: bool = False
    user_activities_choice_correct: bool = False
    choice: str = input(config.bot_message_format + lang.CHOOSE_TOPIC)
    match defineCategory(choice):
        case "studying":
            if config.DEBUG:
                print(config.bot_debug_format + "[DEBUG] Category selected: Studying ")
            while not is_struggling_correct:
                is_struggling: str = input(config.bot_message_format + lang.IS_STRUGGLING)
                if is_struggling.lower() == "yes":
                    is_struggling_correct = True
                    while not want_to_share_correct:
                        want_to_share: str = input(config.bot_message_format + lang.WANT_TO_SHARE)
                        if want_to_share.lower() == "yes":
                            want_to_share_correct = True
                            print(config.bot_message_format + lang.SUGGESTION_STUDY_GROUP)
                            print(config.bot_message_format + lang.FINAL_ADNOTAION)
                        elif want_to_share.lower() == "no":
                            want_to_share_correct = True
                            print(config.bot_message_format + lang.SUGGESTION_STUDENT_ADVISOR)
                            print(config.bot_message_format + lang.FINAL_ADNOTAION)
                        else:
                            print(config.bot_message_error_cancel_format + lang.YES_NO_INCORRECT_RESPONSE.format(username=username))
                elif is_struggling.lower() == "no":
                    is_struggling_correct = True
                    print(config.bot_message_format + lang.SUGGESTION_STUDENT_DESK)
                    print(config.bot_message_format + lang.FINAL_ADNOTAION)
                else:
                    print(config.bot_message_error_cancel_format + lang.YES_NO_INCORRECT_RESPONSE.format(username=username))
            print(config.bot_message_error_cancel_format + lang.END_CONVERSATION.format(end_keyword=config.END_KEYWORD))
        case "sports":
            if config.DEBUG:
                print(config.bot_debug_format + "[DEBUG] Category selected: Sports")
            while not has_specific_sport_correct:
                has_specific_sport: str = input(config.bot_message_format + lang.HAS_SPECIFIC_SPORT)
                if has_specific_sport.lower() == "yes":
                    has_specific_sport_correct = True
                    user_sport: str = input(config.bot_message_format + lang.QUESTION_SPECIFIC_SPORT)
                    if user_sport.lower() in data_sports:
                        print(config.bot_message_format + lang.SUGGESTION_SPORTS_CENTRE)
                        print(config.bot_message_format + lang.FINAL_ADNOTAION)
                    else:
                        print(config.bot_message_format + lang.SPORT_NOT_AVAILABLE)
                        for i in data_sports:
                            print(f"  -> {i}")
                        print(config.bot_message_format + lang.FINAL_ADNOTAION)
                elif has_specific_sport.lower() == "no":
                    has_specific_sport_correct = True
                    sport_fit: str = input(config.bot_message_format + lang.SPORT_FIT)
                    findSport(sport_fit)
                else:
                    print(config.bot_message_format + lang.YES_NO_INCORRECT_RESPONSE)

            print(config.bot_message_error_cancel_format + lang.END_CONVERSATION.format(end_keyword=config.END_KEYWORD))
        case "social activities":
            if config.DEBUG:
                print(config.bot_debug_format + "[DEBUG] Category selected: Activities }")
            while not user_activities_choice_correct:
                user_activities_choice: str = input(config.bot_message_format + lang.EVENTS_OR_ASSOCIATIONS)
                if user_activities_choice.lower() == "events":
                    user_activities_choice_correct = True
                    upcomingEvents(data_events)
                elif user_activities_choice.lower() == "associations":
                    user_activities_choice_correct = True
                    association_fit: str = input(config.bot_message_format + lang.ASSOCIATION_FIT)
                    findAssociation(association_fit)  # TODO
                else:
                    print(config.bot_message_error_cancel_format + lang.EVENTS_OR_ASSOCIATIONS_ERROR)

            print(config.bot_message_error_cancel_format + lang.END_CONVERSATION.format(end_keyword=config.END_KEYWORD))
        case "not found":
            print(config.bot_message_error_cancel_format + lang.CATEGORY_NOT_DEFINED.format(username=username))
            print(config.bot_message_error_cancel_format + lang.END_CONVERSATION.format(end_keyword=config.END_KEYWORD))
        case "stop conversation":
            print(config.bot_message_format + lang.END_MESSAGE.format(username=username))
            conversation_status = False
