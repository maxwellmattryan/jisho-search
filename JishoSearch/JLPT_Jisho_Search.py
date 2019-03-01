# TODO:
# plan program design (identify part of speech, is kanji usually used, etc)
# input error handling for any input

# libraries
import string
from bs4 import BeautifulSoup
import requests

def isValidJLPT(level):
    level = level.lower()
    if(level == "n5" or level == "n4" or level == "n3" or level == "n2" or level == "n1"):
        return True
    elif(level == "five" or level == "four" or level == "three" or level == "two" or level == "one"):
        return True
    else:
        return False

def main():
    
    jlptLevel = input("Please enter JLPT level: ")
    while(isValidJLPT(jlptLevel) == False):
        print("ERROR: " + "\"" + jlptLevel + "\" is an invalid input" + "\n")
        jlptLevel = input("Please enter JLPT level: ")

    url = "https://jisho.org" + "/search/jlpt%20" + jlptLevel + "%20%23words"
    print(url)

    pageResponse = requests.get(url)
    soup = BeautifulSoup(pageResponse.text, "html.parser")

    data = []
    div = soup.find('div', { 'class' : 'concept_light clearfix'})

    for furigana in div.find('span', { 'class' : 'furigana' }):
        print(furigana)

    for kanji in div.find('span', { 'class' : 'text' }):
        print(kanji)

    for meaning in div.find('span', { 'class' : 'text' }):
        print(meaning)

main()