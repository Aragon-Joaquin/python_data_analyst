from enum import Enum

class COLORS(Enum):
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    MAGENTA = '\033[35m'
    CYAN    = '\033[36m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    LIGHT_GRAY = '\033[37m'
    RESET = '\033[0m'


def ColorPrint(msg: str,color: COLORS):
    print(f"{color.value}{str(msg)}{COLORS.RESET.value}\n")