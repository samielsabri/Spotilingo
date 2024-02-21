import re
from unidecode import unidecode
from alphabet_detector import AlphabetDetector

ad = AlphabetDetector()

def process_input(track_name, artist_name):
   """Remove special characters and spaces, and convert to lowercase."""
   track_name = track_name.lower()
   track_name = track_name.split(" (con")[0].strip()
   track_name = track_name.replace("'", "")
   track_name = track_name.replace("’", "")
   track_name = normalize_diacritics_and_special_chars(track_name)
   track_name = re.sub(r"\s+", "-", track_name)
   track_name = track_name.split("-ao-vivo")[0].strip()

   artist_name = artist_name.lower()
   artist_name = artist_name.replace("'", "")
   artist_name = artist_name.replace("’", "")
   artist_name = normalize_diacritics_and_special_chars(artist_name)
   artist_name = artist_name.replace(' ', '-')
   return track_name.lower().strip(), artist_name.lower().strip()

def normalize_diacritics_and_special_chars(string):
   """Normalize diacritics and special characters."""
   # Detect the script used in the string
   result = ""
   for char in string:
       char_script = ad.detect_alphabet(char)
       if "LATIN" in char_script:
           # If the character is a Latin alphabet character, unidecode it
           result += unidecode(char)
       else:
           result += char


   # string_script = ad.detect_alphabet(string)
  
   # if "LATIN" in string_script:
   #     # Initialize an empty string to store the result
   #     result = ""


   #     for char in string:
   #         if 'a' <= char <= 'z' or 'A' <= char <= 'Z':
   #             # If the character is a Latin alphabet character, unidecode it
   #             result += unidecode(char)
   #         else:
   #             # If the character doesn't belong to the Latin script, keep it
   #             result += char
   # else:
   #     # If the script is not Latin, keep the original string
   #     result = string


   return result


def process_track_name_features(track_name):
   """Remove the features from the track name."""
   track_name = track_name.split("-feat")[0].strip()
   track_name = track_name.split("-ft")[0].strip()
   track_name = track_name.split("-ft.")[0].strip()
   track_name = track_name.split("(with")[0].strip()
   return track_name


def preprocess_full_title(title):
   """Remove special characters and spaces, and convert to lowercase."""
   return title.split('by')[0].strip().lower().replace(' ', '-').replace(u'\xa0', u'').replace(u'\u200b', u'').replace(u'\u200e', u'').replace(u'\u200f', u'')
