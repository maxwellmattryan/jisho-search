# TODO:
# fix error of not properly displaying items per page (one of the loop conditions, same words show up regardless of specified jlpt level 
#   something must be happening to URL (?), debug later...)
# delete all print statements

# libraries
import string
import requests
import xlwt
import lxml
from bs4 import BeautifulSoup

# global variable(s)
pageNum = 0
jlptLevel = ""

# asks user for desired jlpt level, handles input error
def getJlptLevel():
    level = input("Please enter JLPT level: ")
    level = changeInput(level)
    while(isValidJLPT(level) == False):
        print("ERROR: " + "\"" + level + "\" is an invalid input" + "\n")
        level = input("Please enter JLPT level: ")
        level = changeInput(level)
    return(level)

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

# function for getting input, called in soup object declaration
def getUrl(level):
    global pageNum
    url = ""
    pageNum += 1
    url = "https://jisho.org" + "/search/jlpt%20" + level + "%20%23words?page=" + str(pageNum)
    return(url)

# initializes xls spreadsheet with proper formatting and returns book, sheet, meaningFx, and regularFx
def initXls(level):
    # creates xls spreadsheet
    level += "Words"
    book = xlwt.Workbook()
    sheet = book.add_sheet(level, True)

    # header format style (wrapped / bold font, centered)
    headingStyle = xlwt.XFStyle()
    headingStyle.font.bold = True
    headingStyle.alignment.wrap = 1
    headingStyle.alignment.vert = xlwt.Alignment.VERT_CENTER
    headingStyle.alignment.horz = xlwt.Alignment.HORZ_CENTER

    # meaning format style (regular font, left justified)
    meaningStyle = xlwt.XFStyle()
    meaningStyle.alignment.wrap = 1
    meaningStyle.alignment.vert = xlwt.Alignment.VERT_CENTER
    meaningStyle.alignment.horz = xlwt.Alignment.HORZ_LEFT

    # regular format style (regular font, centered)
    elseStyle = xlwt.XFStyle()
    elseStyle.alignment.wrap = 1
    elseStyle.alignment.vert = xlwt.Alignment.VERT_CENTER
    elseStyle.alignment.horz = xlwt.Alignment.HORZ_CENTER

    # create header cells and format accordingly
    sheet.row(0).height_mismatch = True
    sheet.row(0).height = 30 * 20
    sheet.write(0, 0, "KANJI", headingStyle)
    sheet.col(0).width = 15 * 367
    sheet.write(0, 1, "FURIGANA", headingStyle)
    sheet.col(1).width = 15 * 367
    sheet.write(0, 2, "MEANING(S)", headingStyle)
    sheet.col(2).width = 90 * 367
    sheet.write(0, 3, "PART OF SPEECH", headingStyle)
    sheet.col(3).width = 30 * 367
    sheet.write(0, 4, "COMMON", headingStyle)
    sheet.col(4).width = 15 * 367

    return (book, sheet, meaningStyle, elseStyle)

# iterates through all entries until empty
def scrape(soup):
    # initialize spreadsheet in scrape() for access
    book, sheet, meaningFx, regularFx = initXls(jlptLevel)

    # keeps track of row in the Excel spreadsheet
    rowIndex = 1

    while(not soup.find('div', {'id' : 'no-matches'})):
        for entry in soup.find_all('div', {'class' : 'concept_light clearfix'}):
            sheet.row(rowIndex).height_mismatch = True
            sheet.row(rowIndex).height = 60 * 20

            kanji = entry.find('span', {'class' : 'text'}).text.strip()
            sheet.write(rowIndex, 0, kanji, regularFx)

            furigana = ""
            kanaIndex = 1
            furiganaWrapper = entry.find('div', {'class' : 'concept_light-representation'}).find_all('span')
            while(kanaIndex < len(furiganaWrapper) - 1):
                furigana += furiganaWrapper[kanaIndex].text.strip()
                kanaIndex += 1
            sheet.write(rowIndex, 1, furigana, regularFx)

            meanings = []
            meaningIndex = 0
            meaningsWrapper = entry.find('div', {'class' : 'meanings-wrapper'})
            while (meaningIndex < len(meaningsWrapper.find_all('div', {'class' : 'meaning-tags'})) and (meaningsWrapper.find_all('div', {'class' : 'meaning-tags'})[meaningIndex].text.strip() != "Wikipedia definition" or 
                   meaningsWrapper.find_all('div', {'class' : 'meaning-tags'})[meaningIndex].text.strip() != "Wikipedia definition")):
                meanings.append("Meaning " + "%02d" % (meaningIndex + 1) + ": " + 
                                meaningsWrapper.find_all('span', {'class' : 'meaning-meaning'})[meaningIndex].text.strip() + "\n")
                meaningIndex += 1
            meanings[len(meanings) - 1] = meanings[len(meanings) - 1].strip()
            sheet.write(rowIndex, 2, meanings, meaningFx)

            partOfSpeech = entry.find_all('div', {'class' : 'meaning-tags'})[0].text.strip()
            sheet.write(rowIndex, 3, partOfSpeech, regularFx)

            isCommon = False
            if(len(entry.find('div', {'class' : 'concept_light-status'}).find_all('span')) > 0 and 
               entry.find('div', {'class' : 'concept_light-status'}).find_all('span')[0].text.strip() == "Common word"):
                isCommon = True
            sheet.write(rowIndex, 4, str(isCommon), regularFx)

            # update row index for spreadsheet
            rowIndex += 1

            # saves book, in innermost loop for safety in case of error, crash, etc.
            book.save("JLPT_Words.xls")

            print ("Kanji: " + kanji)
            print("Furigana: " + furigana)
            for meaning in meanings:
                print(meaning)
            print("Part of Speech : " + partOfSpeech)
            print("Common: " + str(isCommon))
            print()

        # output simple feedback of progress
        print("PAGE: " + str(pageNum) + "\n")
        
        # reset soup object with updated url (new page numbers), call scrape() again
        soup = BeautifulSoup(requests.get(getUrl(jlptLevel), "html.parser").text, "lxml")

def main():
    jlptLevel = getJlptLevel()
    scrape(BeautifulSoup(requests.get(getUrl(jlptLevel), "html.parser").text, "lxml"))

if __name__ == "__main__":
    main()