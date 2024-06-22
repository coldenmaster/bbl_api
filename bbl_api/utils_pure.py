import time

def timer(func):
    def func_in():
        startTime = time.time()
        rt = func()
        print("耗时: %.03f 秒" % (time.time() - startTime))
        return rt
    return func_in

def progress_bar(total):
    for i in range(total + 1):
        progress = i / total * 100
        print(f"\rProgress: [{('#' * int(progress / 10)).ljust(10)}] {progress:.2f}%", end="")
        time.sleep(0.1)

class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    GRAY = '\033[90m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

def print_red(msg):
    print(f"{Color.RED}{msg}{Color.RESET}")

def print_white(msg):
    print(f"{Color.WHITE}{msg}{Color.RESET}")

def print_gray(msg):
    print(f"{Color.GRAY}{msg}{Color.RESET}")

def print_cyan(msg):
    print(f"{Color.CYAN}{msg}{Color.RESET}")

def print_purple(msg):
    print(f"{Color.PURPLE}{msg}{Color.RESET}")

def print_yellow(msg):
    print(f"{Color.YELLOW}{msg}{Color.RESET}")

def print_blue(msg):
    print(f"{Color.BLUE}{msg}{Color.RESET}")
    
def print_blue_kv(key, msg):
    print(f"{Color.BLUE}{key}{Color.RESET}{msg}")

def print_green(msg):
    print(f"{Color.GREEN}{msg}{Color.RESET}")
    
def print_clear(msg):
    pass

from pprint import pprint, pformat

def _print_blue_pp(msg):
    msg = str(pformat(msg))
    print(f"{Color.BLUE}{msg}{Color.RESET}")

def _print_green_pp(msg):
    print(f"{Color.GREEN}{str(pformat(msg))}\n{Color.RESET}")



_TIME_FORMAT = "%H:%M:%S"
def bbl_now() -> str:
    return now_datetime().strftime(DATE_FORMAT + _TIME_FORMAT)
