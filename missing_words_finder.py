import sys
from string import punctuation
import pprint
import json
from nltk.corpus import cmudict

cmudict = cmudict.dict()

def main():
    haiku = load_haiku("train.txt")
    exceptions = cmudict_missing(haiku)
    build_dict = input("\nManually build an exceptions dictionary/add entries to the dict (y/n)?\n")
    if build_dict.lower() == "n":
        sys.exit()
    else:
        missing_words_dict = make_exceptions_dict(exceptions)
        save_exceptions(missing_words_dict)


def load_haiku(filename):
    #Open and return training corpus of haiku as a set
    with open(filename) as in_file:

        haiku = set(in_file.read().replace("-"," ").split())
        return haiku


def cmudict_missing(word_set):
    """Find and return words in word set missing from cmudict."""
    exceptions = set()

    #write something that gets existing json data to compare with
    # word list etc. later
    with open("missing_words.json") as jObj:
        existing_word_data = json.load(jObj)


    for word in word_set:
        word = word.lower().strip(punctuation)
        if word.endswith("'s") or word.endswith("’s"):
            word = word[:-2]
        if (word not in cmudict) and (word not in existing_word_data):
            exceptions.add(word)




    print("\nexceptions:")
    print(*exceptions, sep='\n')
    print("\nNumber of unique words in haiku corpus = {}".format(len(word_set)))
    print("Number of words in corpus not in cmudict = {}".format(len(exceptions)))
    membership = (1 - (len(exceptions) / len(word_set))) * 100
    print("cmudict membership = {:.1f}{}".format(membership, '%'))

    return exceptions

def make_exceptions_dict(exceptions_set):
    """Returns dictionary of words and sullable counts from a set of words"""
    missing_words = {}
    print("Input # syllables in word. Mistakes can be corrected at end. \n")
    for word in exceptions_set:
        while True:
            num_sylls = input("Enter number syllables in {}:".format(word))
            if num_sylls.isdigit():
                 break
            else:
                print("         Not a valid answer. Enter integer!", file=sys.stderr)
        missing_words[word] = int(num_sylls)
    print()
    pprint.pprint(missing_words,width=1)
    print("\nMake Changes to Dictionary Before Saving?")
    print("""
    0 - Exit and save
    1 - Add a Word of Change a Syllable Count
    2 - Remove a Word
    """)

    while True:
        choice = input("\nEnter choice: ")
        if choice == '0':
            break
        elif choice == '1':
            word = input("\nWord to add or change: ")
            missing_words[word] = int(input("Enter number syllables in {}: "
                                            .format(word)))
        elif choice == '2':
            word = input("\nEnter word to delete: ")
            missing_words.pop(word, None)

    print("\nNew words or syllable changes:")
    pprint.pprint(missing_words, width=1)

    return missing_words

def save_exceptions(missing_words):
    """Save exceptions to a dictionary as json file"""
    
    json_string = json.dumps(missing_words)
    f = open("missing_words.json","a")
    f.write(json_string)
    f.close()

    jobj = open("missing_words.json","r")
    jdat = jobj.read()
    jdat_ls = []

    # THis last chunk of code might be a bit rube goldbergy
    # I might optimize it later.
    # But essentially it gets rid of curly braces so that
    # eventually the json file will just be one dictionary.
    # It basically takes all the key value pairs in the json file
    # and gets rid of all curly braces so that all the key value pairs
    # will be within a single set of curly braces.
    for char in jdat:
        if char != "{" and char != "}":
            jdat_ls.append(char)
        else:
            jdat_ls.append(",")
    jdat_ls.pop(0)
    jdat_ls.pop(-1)
    jdat_ls2 = []
    i = 0
    for char in jdat_ls:
        try:
            if char == "," and jdat_ls[i+1] == ",":
                jdat_ls2.append("")
            else:
                jdat_ls2.append(char)

        except IndexError:
            pass
        i += 1


    jobj.close()

    # but now we dont have any curly braces at the begining or end of
    # the json file's text. so this part puts those in.
    # Now we can add new key value pairs to the json file as a single dictionary
    
    with open("missing_words.json","w") as rewriteObj:
        rewriteObj.write("{")
        for char in jdat_ls2:
            rewriteObj.write(char)
        rewriteObj.write("}")

    print("\nFile saved as missing_words.json")
    sys.exit()



if __name__ == "__main__":
    main()
