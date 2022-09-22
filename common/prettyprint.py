class ansi:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def bold(str):
    return f"{ansi.BOLD}{str}{ansi.ENDC}"

def underline(str):
    return f"{ansi.UNDERLINE}{str}{ansi.ENDC}"

def header(str):
    return f"{ansi.HEADER}{str}{ansi.ENDC}"

def success(str):
    return f"{ansi.GREEN}{str}{ansi.ENDC}"

def fail(str):
    return f"{ansi.RED}{str}{ansi.ENDC}"

def warning(str):
    return f"{ansi.YELLOW}{str}{ansi.ENDC}"

def info(str):
    return f"{ansi.CYAN}{str}{ansi.ENDC}"