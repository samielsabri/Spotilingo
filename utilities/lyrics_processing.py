import re
import unicodedata
from alphabet_detector import AlphabetDetector
from romkan import to_hiragana

ad = AlphabetDetector()

ARABIZI_THRESHOLD = 0.20
ROMAJI_THRESHOLD = 0.90
MIN_LINE_LENGTH = 10

def process_lyrics(lyrics):
    """Process Genius lyrics to remove unwanted lines and characters."""
    if lyrics is None:
        return None

    lines = lyrics.split('\n')


    processed_lyrics = []

    for index, line in enumerate(lines):
        if index == 0:
            continue
        if not line.strip(): # skip empty lines
            continue
        if line.startswith('[') or line.endswith(']'): # skip lines indicating song parts
            continue
        if ad.is_latin(line) and len(line) < MIN_LINE_LENGTH: # skip latin alphabet lines that are too short to analyze
            continue
        if '(' in line and ')' in line:
            line = remove_brackets(line)
        if has_repetitive_pattern(line): # deal with "lalalala" "nananana" etc.
            continue
        if is_not_unique_line(line, processed_lyrics): # skip lines that are already in the list
            continue
        if is_valid_romaji(line.lower()):
            line = line.replace("ō", "ou")
            line = to_hiragana(line)
        if line.startswith("You might also like"):
            line = line.replace("You might also like", "").strip()
        if index == len(lines) - 1:
            line = re.sub(r"\d+(\.\d+)?\s*K?Embed$", "", line)
            line = line.replace("Embed", "")
        if is_not_unique_line(line, processed_lyrics): # skip lines that are already in the list
            continue


        processed_lyrics.append(line)

    return processed_lyrics

def process_alternative_lyrics(lyrics):
    """Process Musixmatch lyrics to remove unwanted lines and characters."""
    if lyrics is None:
        return None
    lines = lyrics.split('\n')


    processed_lyrics = []


    for index, line in enumerate(lines):
        if not line.strip(): # skip empty lines
            continue
        if line.startswith('[') or line.endswith(']'): # skip lines indicating song parts
            continue
        if line.startswith('...'):
            continue
        if ad.is_latin(line) and len(line) < MIN_LINE_LENGTH: # skip latin alphabet lines that are too short to analyze
            continue
        if has_repetitive_pattern(line): # deal with "lalalala" "nananana" etc.
            continue
        if '(' in line and ')' in line:
            line = remove_brackets(line)
        if index == len(lines) - 1:
            line = re.sub(r"\d+(\.\d+)?\s*K?Embed$", "", line, flags=re.MULTILINE)
        if is_valid_romaji(line.lower()):
            line = line.replace("ō", "ou")
            line = to_hiragana(line)
        if line.startswith("You might also like"):
            line = line.replace("You might also like", "").strip()
        if line.startswith('******* This Lyrics is NOT for Commercial use *******'): # skip the rest of the lyrics
            break
        if is_not_unique_line(line, processed_lyrics): # skip duplicate lines
            continue


        processed_lyrics.append(line)


    return processed_lyrics

def remove_brackets(line):
    """Remove text in brackets like "(yeah, yeah)" from the input line."""
    pattern = r"\([^)]*\)"
    cleaned_text = re.sub(pattern,'', line)
    return cleaned_text


def has_repetitive_pattern(line):
    """Check if the input line contains a repetitive patterns like "lalalala"."""
    pattern = re.compile(r'(\b\w+\b)(?:\W+\1\b)+', re.IGNORECASE)
    matches = pattern.findall(line)
    return bool(matches)

def remove_unicode_artifacts(line):
    """Remove Unicode control characters from the input line."""
    return ''.join(char for char in line if not unicodedata.category(char).startswith('C'))



def is_not_unique_line(line, processed_lyrics):
    """Check if the input line is already in the list of processed lyrics."""
    for processed_line in processed_lyrics:
        if line == processed_line:
            return True
    return False


def is_valid_romaji(line):
    """Check if the input line is mostly valid Romaji."""
    line = re.sub(r'[^\w\s]', '', line)
    line = line.replace("ō", "ou")
    words = line.split()


    valid_romaji_syllables = [
        "a", "e", "i", "o", "u",
        "ka", "ku", "ke", "ko", "ki",
        "kka", "kku", "kke", "kko", "kki",
        "ga", "gu", "ge", "go", "gi",
        "ha", "hu", "he", "ho", "hi",
        "ba", "bu", "be", "bo", "bi",
        "pa", "pu", "pe", "po", "pi",
        "ppa", "ppu", "ppe", "ppo", "ppi",
        "ma", "mu", "me", "mo", "mi",
        "na", "nu", "ne", "no", "ni",
        "ra", "ru", "re", "ro", "ri",
        "sa", "su", "se", "so",
        "ssa", "ssu", "sse", "sso",
        "za", "zu", "ze", "zo",
        "ta", "te", "to",
        "tta", "tte", "tto",
        "da", "de", "do",
        "wa", "wo",
        "ya", "yu", "yo",
        "ji", "fu",
        "chi", "cchi", "shi", "sshi",
        "tsu", "ttsu",
        "kya", "kyu", "kyo",
        "gya", "gyu", "gyo",
        "bya", "byu", "byo",
        "pya", "pyu", "pyo",
        "rya", "ryu", "ryo",
        "nya", "nyu", "nyo",
        "mya", "myu", "myo",
        "sha", "shu", "sho",
        "ssha", "sshu", "ssho",
        "cha", "chu", "cho",
        "ccha", "cchu", "ccho"
    ]

    potential_romaji_words = 0
    for word in words:
        # Initialize an index to track the current position in the string
        index = 0


        # Iterate through the input string
        while index < len(word):
            found_syllable = False


            # Check for valid syllables starting from the longest to the shortest
            for syllable in sorted(valid_romaji_syllables, key=len, reverse=True):
                if word[index:].startswith(syllable):
                    index += len(syllable)  # Move the index forward by the syllable length
                    found_syllable = True
                    if index >= len(word):
                        potential_romaji_words += 1
                    break


            # If no valid syllable is found, the input is not valid Romaji
            if not found_syllable:
                break

    if potential_romaji_words == 0:
        return False

    # If we reached the end of the string, it's mostly valid Romaji
    return potential_romaji_words / len(words) > ROMAJI_THRESHOLD


def is_potential_arabizi(lyrics):
    """Check if the input lyrics are potentially written in Arabizi (latinized Arabic)."""
    count = 0


    for line in lyrics:
        # Remove any non-alphanumeric characters except spaces
        line_cleaned = ''.join(c for c in line if c.isalnum() or c.isspace())


        # Check if the line contains a sequence of numbers and letters without spaces
        if any(c.isdigit() and i < len(line_cleaned) - 1 and line_cleaned[i+1].isalpha()
                for i, c in enumerate(line_cleaned)):
            count += 1




    return count / len(lyrics) > ARABIZI_THRESHOLD
