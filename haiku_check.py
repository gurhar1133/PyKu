
import sys
print("Processing ...", file=sys.stderr)
import count_syllables as count
import missing_words_finder as miss



def fiveLine():
    five_line = input("Enter a five syllable line: ")
    return five_line

def sevenLine():
    seven_line = input("Enter a seven syllable line:")
    return seven_line




def main():
    while True:
        print("welcome to haiku trainer!".upper())
        print("Dont use punctuation here though. This is NOT a punctuation trainer after all!")
        first_line = fiveLine()
        second_line = sevenLine()
        third_line = fiveLine()

        err_mess = """You have triggered an error due to use of an unreadable word
or phrase you will now be given a choice to add new words to the dictionary
including word(s) that triggered the error"""

        
        try:
            count1 = count.count_syllables(first_line)
    
            count2 = count.count_syllables(second_line)
        
            count3 = count.count_syllables(third_line)

        except KeyError:
            print(err_mess, file=sys.stderr)
            miss.main()
        
        

        print("Processing ...", file=sys.stderr)
        try:
            if count1 == 5:
                print("valid first line")
            else:
                print("invalid line", file=sys.stderr)

            if count2 == 7:
                print("valid second line")
            else:
                print("invalid line", file=sys.stderr)

            if count3 == 5:
                print("valid third line")
            else:
                print("invalid line", file=sys.stderr)

            if count1 == 5 and count2 == 7 and count3 == 5:
                print("Valid Haiku!")
                print(first_line +"\n\n"+second_line+"\n\n"+third_line+"\n\n", file=sys.stderr)
            else:
                print("NOT A VALID HAIKU TRY AGAIN")
        except UnboundLocalError:
            print("line with erroneous word or phrase unable to process, but now it is in corpus", file=sys.stderr)
            print("your addition to the corpus is valued. thank you. restart the program to write more haiku")
            sys.exit()
            
        
        

if __name__ == "__main__":
    main()
