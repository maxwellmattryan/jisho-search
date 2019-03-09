# Jisho Search

This Python script allows for the scraping of dictionary entries of a given JLPT (Japanese Language Proficiency Test) level from [Jisho.org](https://jisho.org/). The specific data scraped includes kanji, furigana, meaning, part of speech, and commonality. The script outputs both to the console and an excel file according to the specified JLPT level.

Resultant spreadsheets can be found [here](https://drive.google.com/open?id=1BAvCwVEkObtevfx9YwB0gGtDbqpndqsj).

## Libraries 

You will need to install the following libraries in order to run the script.

```
pip install bs4 requests xlwt lxml
```

## Acknowledgments

- This was my first script to utilize web scraping and ended up being quite enjoyable for me.
- Extracting dictionary entries of Japanese words (specifically according to JLPT level) into a spreadsheet is useful for studying for a specific certification of said JLPT level.
- [Jisho.org](https://jisho.org/) is a fantastic resource that has been considerably helpful prior to writing this script - would recommend to anyone interested in or currently learning Japanese.

Please do not hesitate to reach out should you have any questions. Thank you very much for reading !
