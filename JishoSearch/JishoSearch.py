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
    if(isValidJLPT(level) == False):
        print("ERROR: " + "\"" + level + "\" is an invalid input" + "\n")
        getJlptLevel()
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

# asks user if they only want common words written to spreadsheet
def askForCommonWordsOnly():
    boolString = input("\n" + "Would you like only common words (y/n): ")
    boolString = boolString.lower()
    if(boolString == 'y'):
        return True
    elif(boolString == 'n'):
        return False
    else:
        print("ERROR: " + "\"" + boolString + "\" is an invalid input")
        askForCommonWordsOnly()

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
    filename = "JLPT_" + level + ".xls"
    name = level + " Words"
    book = xlwt.Workbook()
    sheet = book.add_sheet(name, True)

    # header format style (wrapped / bold font, centered)
    headingStyle = xlwt.XFStyle()
    headingStyle.font.bold = True
    headingStyle.font.height = 16 * 20
    headingStyle.alignment.wrap = 1
    headingStyle.alignment.vert = xlwt.Alignment.VERT_CENTER
    headingStyle.alignment.horz = xlwt.Alignment.HORZ_CENTER

    # meaning format style (regular font, left justified)
    meaningStyle = xlwt.XFStyle()
    meaningStyle.font.height = 11 * 20
    meaningStyle.alignment.wrap = 1
    meaningStyle.alignment.vert = xlwt.Alignment.VERT_CENTER
    meaningStyle.alignment.horz = xlwt.Alignment.HORZ_LEFT

    # regular format style (regular font, centered)
    elseStyle = xlwt.XFStyle()
    elseStyle.font.height = 16 * 20
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

    return (filename, book, sheet, meaningStyle, elseStyle)

# iterates through all entries until empty
def scrapeAndWrite(soup, level):
    # prompt user for only common words
    commonWordsOnly = askForCommonWordsOnly()

    # initialize spreadsheet in scrape() for access
    file, book, sheet, meaningFx, regularFx = initXls(level)

    # keeps track of row in spreadsheet
    rowIndex = 0

    while(not soup.find('div', {'id' : 'no-matches'})):
        for entry in soup.find_all('div', {'class' : 'concept_light clearfix'}):
            kanji = entry.find('span', {'class' : 'text'}).text.strip()

            furiganaSet = []
            for furiganaElement in entry.find_all('span', {'class' : 'furigana'}):
                if(len(furiganaElement.find_all('rt')) > 0):
                    furiganaSet.append(furiganaElement.find('rt').text.strip())
                    break
                for furigana in furiganaElement.find_all('span'):
                    if(furigana.text.strip() == ""):
                        continue
                    furiganaSet.append(furigana.text.strip())

            furigana = kanji
            furiganaIndex = 0
            furiganaSetIndex = 0
            while(furiganaIndex < len(furigana) and furiganaSetIndex < len(furiganaSet)):
                if(furigana[furiganaIndex] > 'ヿ'):
                    furigana= furigana.replace(furigana[furiganaIndex], furiganaSet[furiganaSetIndex])
                    furiganaSetIndex += 1
                furiganaIndex += 1
            for kana in furigana:
                if(kana > 'ヿ'):
                    furigana = furigana.replace(kana, "")

            meanings = []
            meaningWrappers = entry.find_all('div', {'class' : 'meaning-wrapper'})
            wrapperCount = len(meaningWrappers)
            while(wrapperCount > 0):
                if(meaningWrappers[len(meaningWrappers) - wrapperCount].find('span', {'class' : 'break-unit'}) or len(meaningWrappers) - wrapperCount > 4):
                    break
                if(len(meaningWrappers[len(meaningWrappers) - wrapperCount].find_all('span', {'class': 'meaning-meaning'})) > 0):
                    meanings.append("Meaning " + "%02d" % (len(meaningWrappers) - wrapperCount + 1) + ": " +
                                meaningWrappers[len(meaningWrappers) - wrapperCount].find('span', {'class': 'meaning-meaning'}).text.strip() + "\n")
                wrapperCount -= 1
            meanings[len(meanings) - 1] = meanings[len(meanings) - 1].strip()

            if(len(entry.find_all('div', {'class' : 'meaning-tags'})) >= 1):
                partOfSpeech = entry.find_all('div', {'class' : 'meaning-tags'})[0].text.strip()
            else:
                partOfSpeech = "NONE"

            isCommon = False
            if(len(entry.find('div', {'class' : 'concept_light-status'}).find_all('span')) > 0 and 
               entry.find('div', {'class' : 'concept_light-status'}).find_all('span')[0].text.strip() == "Common word"):
                isCommon = True

            # update row index for spreadsheet
            rowIndex += 1

            # format spreadsheet
            sheet.row(rowIndex).height_mismatch = True
            sheet.row(rowIndex).height = 75 * 20

            # write to spreadsheet, check for commonWordsOnly
            if(commonWordsOnly and not isCommon):
                break
            else:
                sheet.write(rowIndex, 0, kanji, regularFx)
                sheet.write(rowIndex, 1, furigana, regularFx)
                sheet.write(rowIndex, 2, meanings, meaningFx)
                sheet.write(rowIndex, 3, partOfSpeech, regularFx)
                sheet.write(rowIndex, 4, isCommon, regularFx)

            # save spreadsheet, in innermost loop for safety in case of error, crash, etc.
            book.save(file)

            # print to console for checking
            print()
            print ("Kanji: " + kanji)
            print("Furigana: " + furigana)
            for meaning in meanings:
                meaning = meaning.strip()
                print(meaning)
            print("Part of Speech: " + partOfSpeech)
            print("Common: " + str(isCommon))
            print()

        # output simple feedback of progress
        print("RESULTS OF PAGE: " + "%03d" % (pageNum) + "\n\n" + "--------------------" + "\n")
        
        # reset soup object with updated url (new page numbers), call scrape() again
        soup = BeautifulSoup(requests.get(getUrl(level), "html.parser").text, "lxml")
    return

def main():
    jlptLevel = getJlptLevel()
    scrapeAndWrite(BeautifulSoup(requests.get(getUrl(jlptLevel), "html.parser").text, "lxml"), jlptLevel)

if __name__ == "__main__":
    main()