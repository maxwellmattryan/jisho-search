# TODO:
# create class, "Word", with furigana (if furigana ...), kanji (if kanji, is usually written with kana), meaning (first and maybe second
# section of meanings), isCommon, part of speech (enum ?, also if verb then what kind)
# pull correct data from website page source

# libraries
import string
from bs4 import BeautifulSoup
import requests

# word class
class Word():
    # initialize function
    def __init__(self):
        self.furigana = ""
        self.kanji = ""
        self.meaning = ""
        self.isCommon = False
        self.type = ""

# function for getting input, called in soup object declaration
def getURL():
    jlptLevel = input("Please enter JLPT level: ")
    jlptLevel = changeInput(jlptLevel)
    while(isValidJLPT(jlptLevel) == False):
        print("ERROR: " + "\"" + jlptLevel + "\" is an invalid input" + "\n")
        jlptLevel = input("Please enter JLPT level: ")
        jlptLevel = changeInput(jlptLevel)
    url = "https://jisho.org" + "/search/jlpt%20" + jlptLevel + "%20%23words"

    # print tests, delete later
    print(jlptLevel)
    print(url)

    return (url)

# if user entered number in word form, change for proper search results
def changeInput(level):
    temp = level.lower()
    if(temp == "one"):
        return "N1"
    elif(temp == "two"):
        return "N2"
    elif(temp == "three"):
        return "N3"
    elif(temp == "four"):
        return "N4"
    elif(temp == "five"):
        return "N5"
    else:
        return level

# checking if proper JLPT level
def isValidJLPT(level):
    level = level.lower()
    if(level == "n5" or level == "n4" or level == "n3" or level == "n2" or level == "n1"):
        return True
    else:
        return False

def main():

    # gather html object with beautiful soup and requests library\
    soup = BeautifulSoup(requests.get(getURL()).text, "html.parser")

    data = []
    div = soup.find('div', { 'class' : 'concept_light clearfix'})

    for furigana in div.find('span', { 'class' : 'furigana' }):
        print(furigana)

    for kanji in div.find('span', { 'class' : 'text' }):
        print(kanji)

    for meaning in div.find('span', { 'class' : 'text' }):
        print(meaning)

if __name__ == "__main__":
    main()