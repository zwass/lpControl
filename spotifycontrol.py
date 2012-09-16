import logging
from subprocess import (Popen, PIPE, call)

logger = logging.getLogger(__name__)

def runscript(script):
    """
    Run the provided AppleScript (with no error handling)
    """
    try:
        call(["osascript", "-e", script])
    except:
        logging.exception("Exception calling script: %s" % script)

def play():
    script = """
    tell application "Spotify"
    play
    end tell
    """
    runscript(script)

def pause():
    script = """
    tell application "Spotify"
    pause
    end tell
    """
    runscript(script)

def next():
    script = """
    tell application "Spotify"
    next track
    end tell
    """
    runscript(script)

def prev():
    script = """
    tell application "Spotify"
    previous track
    end tell
    """
    runscript(script)
