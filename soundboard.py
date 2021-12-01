# Soundboard
import random

sound_dir = "sounds/"
sounds = {"bruh": "bruh",
          "deja vu": "deja-vu",
          "among us": "among-us",
          "thud": "thud",
          "ttt": "ttt",
          "gas gas gas": "gas-gas-gas",
          "machi": "machi",
          "u got that": "u-got-that",
          "wide": "wide",
          "dog": "what-the-dog-doin",
          "oof": "oof",
          "sad": "sad-violin",
          "bass": "bass",
          "nice cock": "nice-cock",
          "bing chilling": "bing-chilling",
          "stfu": "stfu",
          "ali a": "ali-a",
          "sui": "sui"
          }


def get_sound_path(sound_name):
    if sound_name == "random":
        choice = random.choice(list(sounds.keys()))
        print(choice)
        return sound_dir + sounds[choice] + ".mp3"
    elif sound_name in sounds.keys():
        return sound_dir + sounds[sound_name] + ".mp3"
    else:
        return None


def play_sound():
    play_sound()


def stop_sound():
    stop_sound()
