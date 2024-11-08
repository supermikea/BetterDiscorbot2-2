import sys

class log:

    def __init__(self, loglevel=0, classname="NO CLASSNAME SPECIFIED") -> None:
        self.loglevel = loglevel
        self.className = classname

    def __call__(self, prefix, message, classname=""):
        return self.log(prefix, message, classname,)

    def log(self, prefix, message, className=""): # return if loglevel is less then required
        if not className:
            className == self.className
        if self.loglevel == 0:
            return
        if prefix == "warning" or prefix == "error":
            if not self.loglevel > 0:
                return
        elif prefix == "info":
            if not self.loglevel > 1:
                return
        elif prefix == "verbose" or prefix == "debug":
            if not self.loglevel > 2:
                return
        print(f"[{prefix.upper()}] [{className.upper()}]: {message}")


def trim_string_to_limit(text, limit=2000, append_message=""):
    """
    Trims the string to ensure its length is within the specified limit (default 2000).
    If the text length exceeds the limit, it removes lines from the end until the length is within the limit,
    then appends a specified message at the end of the trimmed text.

    Parameters:
    text (str): The input text string.
    limit (int): The maximum length of the string.
    append_message (str): The message to append if the text is trimmed.

    Returns:
    tuple: The trimmed string with the append_message (if trimmed), and the number of lines removed.
    """
    # Split the text into lines
    lines = text.splitlines()
    original_line_count = len(lines)
    
    # Loop to trim lines from the end until length is within limit
    while len('\n'.join(lines)) + len(append_message) > limit:
        lines.pop()  # Remove the last line
    
    # Calculate the number of lines removed
    lines_removed = original_line_count - len(lines)

    # Join lines and add the message if any lines were removed
    result = '\n'.join(lines) + (append_message if lines_removed > 0 else "")
    
    return result, lines_removed
