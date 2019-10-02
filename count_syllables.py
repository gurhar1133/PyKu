import sys
from string import punctuation
import json
from nltk.corpus import cmudict
with open("missing_words.json") as f:
    missing_words = json.load(f)

cmudict = cmudict.dict()

def count_syllables(words):
    # this will use corpora to count syllables of given word or phrase
    words = words.replace("-"," ")
    words = words.lower().split()
    num_sylls = 0
    for word in words:
        word = word.strip(punctuation)
        if word.endswith("'s"):
            word = word[:-2]
        if word in missing_words:
            num_sylls += missing_words[word]
        else:
            for phonemes in cmudict[word][0]:
                for phoneme in phonemes:
                    if phoneme[-1].isdigit():
                        num_sylls += 1
    return num_sylls


def main():
    while True:
        print("Syllable Counter")
        word = input("Enter word or phrase; else press Enter to Exit: ")
        if word == "":
            sys.exit()
        try:
            num_syllables = count_syllables(word)
            print("number of syllables in {} is: {}".format(word,num_syllables))
        except KeyError:
            print("A word you used was not found. You probably used an invalid word. Try again. \n", file=sys.stderr)
            print("Sorry I am a stupid robot")



if __name__ == "__main__":
    main()
