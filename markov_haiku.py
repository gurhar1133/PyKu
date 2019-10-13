import sys
import logging
import random
from collections import defaultdict
from count_syllables import count_syllables

# logging.disable(logging.CRITICAL)

logging.basicConfig(level=logging.DEBUG, format="%(message)s")

def load_training_file(file):
    """returns the text file as a string"""
    with open(file) as f:
        raw_haiku = f.read()
        # returns the string from the text file. This helps
        # us build the training corpus
        return raw_haiku


def prep_training(raw_haiku):
    """Loads the raw string and removes newlines, splits on the
        basis of spaces and returns a word list"""
    # this replaces newlines with spaces because words dont
    # extend over lines, then makes and returns a list of
    # the words called corpus
    corpus = raw_haiku.replace("\n"," ").split()
    return list(corpus)


def map_word_to_word(corpus):
    """ creates a dictionary mapping of words and the words
        that follow them eg "prefix":"suffix" """
    # this sets an indexing limit so we avoid an IndexError
    limit = len(corpus)-1

    # this initializes a dictionary that will have lists as
    # values
    dict1_to_1 = defaultdict(list)

    # the for loop iterates over each word in the corpus
    # and keeping track of the current index (and whether it
    # is within the limit) adds key value pairs to the dictionary
    # initialized above
    for index, word in enumerate(corpus):
        if index < limit:
            # suffix is the word following the current word
            suffix = corpus[index + 1]
            # this appends suffix words to the value list
            dict1_to_1[word].append(suffix)
    logging.debug("map_word_to_word results for \"sake\" = %s\n",
                  dict1_to_1["sake"])
    # the dictionary is then returned
    return dict1_to_1



def map_2_words_to_word(corpus):
    """Loads the word list and maps two words to the words that
        follow that word pair (very similar to the function above)"""
    # we now have to change the limit
    limit = len(corpus) - 2

    dict2_to_1 = defaultdict(list)

    for index, word in enumerate(corpus):
        if index < limit:
            # set the key to the current word concatenated with a space
            # and the next word in the list
            key = word + " " + corpus[index + 1]

            # set the suffix to word that follows the two words that were
            # just stored in "key"
            suffix = corpus[index + 2]

            # adds the values to the dictionary
            dict2_to_1[key].append(suffix)

    logging.debug("map_2_words_to_word results for \"sake jug\"=%\n",
                  dict2_to_1["sake jug"])
            

    return dict2_to_1

def random_word(corpus):
    """ This function takes the corpus as input returns a random word
        and its syllable count. """
    word = random.choice(corpus)
    num_sylls = count_syllables(word)

    if num_sylls > 4:
        # we dont want words with too many sylablles to be a first line
        # of a haiku and we dont want single word lines. Hence the
        # if num_sylls > 4 leading to recursivly calling random_word()
        random_word(corpus)
    else:
        logging.debug("random word & syllables = %s %s\n",word,num_sylls)
        return (word,num_sylls)



def word_after_single(prefix, suffix_map_1, current_sylls, target_sylls):
    """This should return all the appropriate words in a corpus which
        follow from a single word seed"""
    accepted_words = []

    # creates a list of possible suffixes based on the prefix
    suffixes = suffix_map_1.get(prefix)

    if suffixes != None:
        for candidate in suffixes:
            # counts the syllables of each suffix candidate word
            num_sylls = count_syllables(candidate)
            if current_sylls + num_sylls <= target_sylls:
                # if the current syllable count plus the suffix candidate
                # suffix count is less than or equal to our syllable goal
                # count, then add it to accepted words. Basically, check
                # if the suffix candidate is acceptable in terms of
                # syllable count
                accepted_words.append(candidate)

    logging.debug("1 accepted words after\"%s\" = %s\n", prefix, set(accepted_words))
    return accepted_words



def word_after_double(prefix, suffix_map_2, current_sylls, target_sylls):
    """ This function should return all the approprate words in a corpus
        that follow from the preceding two words. Follows a very similar
        logical structure to 'word_after_single'"""
    accepted_words = []
    
    suffixes = suffix_map_2.get(prefix)
    
    if suffixes != None:
        for candidate in suffixes:
            num_sylls = count_syllables(candidate)
            if current_sylls + num_sylls <= target_sylls:
                accepted_words.append(candidate)
   
    logging.debug("2 accepted words after \"%s\" = %s\n",
                  prefix, set(accepted_words))
    return accepted_words


def haiku_line(suffix_map_1, suffix_map_2, corpus, end_prev_line,
               target_sylls):
    """This function builds haiku lines from the training corpus"""
    line = "2/3"
    line_sylls = 0

    # this initializes a list to build a haiku line
    current_line = []
    
    if len(end_prev_line) == 0:
        line = "1"
        # have to declare two variables in this line because
        # random_word returns both a word and a syllable count
        # on that word
        word, num_sylls = random_word(corpus)
        # then it adds that word to the current line
        current_line.append(word)
        # and increments the syllable count accordingly
        line_sylls += num_sylls
        # then word_after_single is called to return
        # the words that appear in the corpus after the seed word
        word_choices = word_after_single(word, suffix_map_1, line_sylls,
                                         target_sylls)
        
        
        while len(word_choices) == 0:
            # this while loop handles situations where our
            # list of suffixes is empty and gives us a non_empty one
            prefix = random.choice(corpus)
            logging.debug("3 new random prefix = %s", prefix)
            word_choices = word_after_single(prefix, suffix_map_1,
                                             line_sylls, target_sylls)
        word = random.choice(word_choices)
        num_sylls = count_syllables(word)
        logging.debug("word & syllables = %s %s", word, num_sylls)
        line_sylls += num_sylls
        current_line.append(word)
        if line_sylls == target_sylls:
                # end_prev_line will be the prefix for the next line
                # it is just the last two words of the first line
                # and helps us generate the second line
            end_prev_line.extend(current_line[-2:])
                
            return current_line, end_prev_line
    else:
                # build more dang lines
        current_line.extend(end_prev_line)

    while True:
        logging.debug("line = %s\n", line)
        prefix = current_line[-2] + " " + current_line[-1]
        word_choices = word_after_double(prefix, suffix_map_2,
                                                 line_sylls, target_sylls)
        print(word_choices)
                # if we have an empty list for word_choices, then
                # we pick new two word prefixes untill we have word
                # choices
        while len(word_choices) == 0:
                    
            index = random.randint(0, len(corpus) -2)
            prefix = corpus[index] + " " + corpus[index + 1]
            logging.debug("4 new random prefix = %s", prefix)
            word_choices = word_after_double(prefix, suffix_map_2,
                                                     line_sylls, target_sylls)
        word = random.choice(word_choices)
        num_sylls = count_syllables(word)
        logging.debug("word and syllables = %s %s", word, num_sylls)

        if line_sylls + num_sylls > target_sylls:
            continue
        elif line_sylls + num_sylls < target_sylls:
            current_line.append(word)
            line_sylls += num_sylls
        elif line_sylls + num_sylls == target_sylls:
            current_line.append(word)
            break

    end_prev_line = []
    end_prev_line.extend(current_line[-2:])

    if line == "1":
        final_line = current_line[:]
    else:
        final_line = current_line[2:]
                    # this removes end_prev_line from the current_line if it is there
            
    return final_line, end_prev_line
            
        
        
def main():
    """Give the user the ability to build/modify haiku"""
    intro = """/n
    wassup? wanna write some haiku? Im a haiku writing robot my dude. \n"""
    print("{}".format(intro))


    raw_haiku = load_training_file("train.txt")
    corpus = prep_training(raw_haiku)
    suffix_map_1 = map_word_to_word(corpus)
    suffix_map_2 = map_2_words_to_word(corpus)
    final = []
    
    choice = None

    while choice != "0":
        print("""
            Haiku Generator
            Here are your options:
            
            0 - quit
            1 - generate haiku
            2 - regenerate line 2
            3 - regenerate line 3
            """
              )


        choice = input("Choice: ")

        print()
        if choice == "0":
            print(":( bye bye")
            sys.exit()

        elif choice == "1":
            final = []
            end_prev_line = []
            first_line, end_prev_line1 = haiku_line(suffix_map_1, suffix_map_2,
                                                    corpus, end_prev_line, 5)
            final.append(first_line)
            line, end_prev_line2 = haiku_line(suffix_map_1, suffix_map_2,
                                              corpus, end_prev_line1, 7)
            final.append(line)
            line, end_prev_line3 = haiku_line(suffix_map_1, suffix_map_2, corpus,
                                              end_prev_line2, 5)
            final.append(line)

        elif choice == "2":
            if not final:
                print("""You have to generate an initial haiku before you
                            can modify lines dude""")
                continue
            else:
                line, end_prev_line2 = haiku_line(suffix_map_1, suffix_map_2,
                                                       corpus, end_prev_line1, 7)
                final[1] = line

        elif choice == "3":
            if not final:
                print("""You have to generate an initial haiku before you
                            can modify lines dude""")
                continue
            else:
                line, end_prev_line3 = haiku_line(suffix_map_1, suffix_map_2,
                                                      corpus, end_prev_line2, 5)
                final[2] = line

        else:
            print("invalid choice!", file=sys.stderr)
            continue
    
        print()
        print("FIRST:", end="")
        print(" ".join(final[0]), file=sys.stderr)
        print("SECOND:", end="")
        print(" ".join(final[1]), file=sys.stderr)
        print("THIRD:", end="")
        print(" ".join(final[2]), file=sys.stderr)
        print()


    input("\n\nPress the Enter key to exit.")


if __name__ == "__main__":
    main()
            
                    
            
