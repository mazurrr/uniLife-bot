
greeting_title: str = """
 _     _         _       ______               
| |   | |       (_)     (____  \         _    
| |   | | ____   _  ___  ____)  )  ___  | |_  
| |   | ||  _ \ | |(___)|  __  (  / _ \ |  _) 
| |___| || | | || |     | |__)  )| |_| || |__ 
 \______||_| |_||_|     |______/  \___/  \___)
                                              
"""


class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def send_msg(msg_type: str, content: str) -> None:
    match msg_type:
        case "default":
            print(f"{config.bot_message_format}{content}")
        case "error":
            print(f"{config.bot_message_error_cancel_format}{content}")
        case "debug":
            print(f"{config.bot_debug_format}{content}")
        case "highlight":
            print("elo")
