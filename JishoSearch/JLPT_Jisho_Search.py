# TODO:
# create dictionary for all words
# write data to excel spreadsheet
# clean up program

# libraries
import string
from bs4 import BeautifulSoup
import requests

# function for getting input, called in soup object declaration
def getURL():
    jlptLevel = input("Please enter JLPT level: ")
    jlptLevel = changeInput(jlptLevel)
    while(isValidJLPT(jlptLevel) == False):
        print("ERROR: " + "\"" + jlptLevel + "\" is an invalid input" + "\n")
        jlptLevel = input("Please enter JLPT level: ")
        jlptLevel = changeInput(jlptLevel)
    url = "https://jisho.org" + "/search/jlpt%20" + jlptLevel + "%20%23words?page=" + str(pageNum)
    return (url)

# if user entered number in word form, change for proper search results
def changeInput(level):
    temp = level.lower()
    temp = temp.strip(" ")
    if(temp == "one" or temp == "1"):
        return "N1"
    elif(temp == "two" or temp == "2"):
        return "N2"
    elif(temp == "three" or temp == "3"):
        return "N3"
    elif(temp == "four" or temp == "4"):
        return "N4"
    elif(temp == "five" or temp == "5"):
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

def updateURL():
    global pageNum
    global url

    pageNum += 1
    url = url[0:len(url) - len(str(pageNum))] + str(pageNum)
    return (url)

def main():
    # global variables
    global jlptLevel
    global pageNum
    global url

    # declarations
    pageNum = 1
    url = getURL()

    # gather html object with beautiful soup and requests library
    soup = BeautifulSoup(requests.get(url).text, "html.parser")

    while(len(soup.find_all('div', {'id' : 'main_results'})) > 0 and not soup.find('div', {'id' : 'no-matches'})):
        for entry in soup.find_all('div', {'class' : 'concept_light clearfix'}):
            kanji = entry.find('span', {'class' : 'text'}).text.strip()
            print ("Kanji: " + kanji)

            furigana = entry.find('div', {'class' : 'concept_light-representation'}).find_all('span')[1].text.strip()
            print ("Furigana : " + furigana)

            meaning = []
            meaning = entry.find_all('div', {'class' : 'meaning-wrapper'})[0].find('span', {'class' : 'meaning-meaning'}).text.strip()
            print("Meaning: " + meaning)

            partOfSpeech = entry.find_all('div', {'class' : 'meaning-tags'})[0].text.strip()
            print(partOfSpeech)

            isCommon = False
            if(len(entry.find('div', {'class' : 'concept_light-status'}).find_all('span')) > 0 and 
               entry.find('div', {'class' : 'concept_light-status'}).find_all('span')[0].text.strip() == "Common word"):
                isCommon = True
            print("Common: " + str(isCommon))

            print("\n")

        soup = BeautifulSoup(requests.get(updateURL()).text, "html.parser")

if __name__ == "__main__":
    main()