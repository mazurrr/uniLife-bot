from assets import utils
from typing import List, Dict

DEBUG: bool = True  # Debug mode for developing purposes
END_KEYWORD: str = "stop conversation"
MIN_REQUIRED_SIMILARITY_SCORE: float = 55.0  # Minimal similarity score in order to select a category
MIN_REQ_SIM_SCORE_MATCH: Dict[str, float] = {
    "associations": 35.0,
    "sports": 35.0,
}
MIN_REQ_SIM_SCORE_FINAL_MATCH: Dict[str, float] = {
    "associations": 60.0,
    "sports": 35.0,
}
USER_INPUT_BLACKLISTED_SIGNS: List[str] = ["?", "!", ",", "."]
DEFINE_CATEGORY_CATEGORIES: List[str] = ["studying", "sports", "social activities"]
message = utils.Color.GREEN  # default bot message format
debug = utils.Color.RED + utils.Color.BOLD  # debug bot message format
error = utils.Color.RED  # error / cancel bot message format
special = utils.Color.PURPLE  # special bot message format
highlight = utils.Color.YELLOW  # highlight bot message format
