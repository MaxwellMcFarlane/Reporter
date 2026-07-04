import os
import numpy as np
import pprint

def check_file_exists(file_path:str) -> bool:
    try:
        with open(file_path, 'r'):
            return True
    except FileNotFoundError:
        return False

def console_log(msg="",msglvl=0,status="info"):
    """
    Prints a string to the console with variable indentation and color
    depending on the msglvl parameter.

    Args:
        msg (str): The string to be printed.
        msglvl (int): The message level (1-5).
                      - Level 1: Low indentation, subtle color (e.g., green for success)
                      - Level 2: Slightly more indentation, info color (e.g., blue)
                      - Level 3: Medium indentation, warning color (e.g., yellow)
                      - Level 4: Higher indentation, error color (e.g., red)
                      - Level 5: Highest indentation, critical color (e.g., magenta)
    """
    # ANSI escape codes for colors and reset
    # See: https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
    COLORS = {
        "pass": "\033[92m",  # Green (Light) - Success/Info
        "info": "\033[94m",  # Blue (Light) - Info
        "warn": "\033[93m",  # Yellow (Light) - Warning
        "err": "\033[91m",  # Red (Light) - Error
        "fatal": "\033[95m",  # Magenta (Light) - Critical
    }
    RESET_COLOR = "\033[0m" # Resets color to default

    # Define indentation level based on msglvl
    # You can adjust the `indent_multiplier` to control spacing
    indent_multiplier = 4 # Spaces per level
    indentation = " " * (msglvl * indent_multiplier)

    # Get the color code, default to no color if msglvl is out of range
    color_code = COLORS.get(status, "")

    # Construct the final string
    # Apply color, then indentation, then message, then reset color
    formatted_message = f"{color_code}{indentation}{msg}{RESET_COLOR}"

    print(formatted_message)

# If path doesn't start with / then it is assumed to be a path from the home work path
# Otherwise, it is either relative or absolute
# If this is a relative path it should be indicated with a ./.. in the leading characters
# Otherwise this is assumed to be an absolute path
def dcc_realpath(path:str="",msglvl=0):
    dcchome = f"{os.environ.get('DCCHOME')}"
    try :
        spl = str.split(path,"/")
        if ("testcase" in spl[1]) or ("backend" in spl[1]) : return f"{dcchome}/{path}"
        elif "/" == path[0]: return path
        else: return os.path.realpath(path)
    except OSError: return None

def is_number(val):
    return isinstance(val, (int, float, np.number)) and not isinstance(val, bool)

# Designed to be used in other python scripts
if __name__ == "__main__":
    pass