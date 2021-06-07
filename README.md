# Jisho Search

___CAUTION__: I have not included any `sleep` methods, so if you use this please be polite to the servers and add it in!_

This Python script allows for the scraping of dictionary entries of a given JLPT (Japanese Language Proficiency Test) level from [Jisho.org](https://jisho.org/). The specific data scraped includes kanji, furigana, meaning, part of speech, and commonality. The script outputs both to the console and an excel file according to the specified JLPT level.

Resultant spreadsheets can be found [here](https://drive.google.com/open?id=1BAvCwVEkObtevfx9YwB0gGtDbqpndqsj).

## How To Use 

### Installation

You will need to install the following libraries in order to run the script.

```
pip install bs4 requests xlwt lxml
```

### Execution

Before starting, make sure you are in the root folder of the repository. Begin by running script with either the `python` or `python3` commands, like:

```
python3 JishoSearch.py
```

This will result in two prompts:

- __JLPT Level__: the intended JLPT level to use in scraping, and the other for if you would like to include __only__ common words (use single digit input or phoenetic spelling)
- __Commonality__: determines if the scraper should include or ignore words that are uncommon but still within the specified JLPT level

The results will be written to a file of the naming convention, `jlpt-n<1..5>.xls`, within a `sheets` directory. Happy scraping!

## Acknowledgments

- This was my first script to utilize web scraping and ended up being quite enjoyable for me.
- Extracting dictionary entries of Japanese words (specifically according to JLPT level) into a spreadsheet is useful for studying for a specific certification of said JLPT level.
- [Jisho.org](https://jisho.org/) is a fantastic resource that has been considerably helpful prior to writing this script - would recommend to anyone interested in or currently learning Japanese.

Please do not hesitate to reach out should you have any questions. Thank you very much for reading !
