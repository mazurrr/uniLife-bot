from assets import utils

DEBUG: bool = False  # Debug mode for developing purposes
END_KEYWORD: str = "stop conversation"
MIN_REQUIRED_SIMILARITY_SCORE: float = 35.0  # Minimal similarity score in order to select a category
MIN_REQ_SIM_SCORE_ASSOCIATIONS_WORD_MATCH: float = 35.0
MIN_REQ_SIM_SCORE_ASSOCIATIONS_FINAL_MATCH: float = 60.0
bot_message_format = utils.Color.GREEN
bot_debug_format = utils.Color.RED + utils.Color.BOLD
bot_message_error_cancel_format = utils.Color.RED
bot_message_special_format = utils.Color.PURPLE
bot_message_date_highlight = utils.Color.YELLOW
