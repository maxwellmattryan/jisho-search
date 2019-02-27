# library imports
from bs4 import BeautifulSoup
import requests

def main():

    # todo: plan program design and modularize it
    # todo: input errors / exceptions
    
    url = "https://jisho.org/"
    jlptLevel = input("Please enter JLPT level: ")
    print(url + " : " + jlptLevel)

    pageResponse = requests.get(url, verify = False)
    print(pageResponse)

if __name__ == "__main__":
  main()