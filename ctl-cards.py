#!/usr/bin/env python


"""
This script will download all of the PDF flashcard packs from the Come
to Live website and create 500x500 JPEG versions of each card. All of
this will be stored in a directory called CTL-Flashcards in the user's
$HOME directory.

Presently, the conversion from CMYK PDFs to RGB JPEGs causes some color
distortion that is only partially fixed by adjustments to brightness,
saturation, and hue. A future version of this script will ideally have
that sorted out properly.
"""


__appname__ = "ctl-cards"
__author__  = "Christopher Perry"
__email__   = "ozbonus@gmail.com"
__version__ = "1.1"
__license__ = "MIT License"


import urllib.request
import urllib.error
import os
import re
import PyPDF2
from wand.image import Image


HOME = os.path.expanduser("~")
BASEPATH = HOME + "/CTL-Flashcards/"


def prepare_directory():
    """
    Check if the necessary directory and subdirectory exist and create
    them if they do not.
    """
    try:
        if os.path.isdir(BASEPATH):
            print("CTL-Flashcards directory exists, proceeding there.")
        else:
            print("CTL-Flashcards directory does not exist, so it will be created.")
            os.mkdir(BASEPATH)
            os.mkdir(BASEPATH + "Singles/")
    except:
        print("Something went wrong while checking for the CTL-Flashcards directory.")


def download_cards(book, unit):
    """
    This function will attempt to download the corresponding pdf of
    vocabulary cards for a given book and unit. If a 404 error is
    returned, it is assumed that the given book does not have a unit of
    that number. This is printed to the console without exiting the
    script. Other HTML errors will be printed to the console and exit
    the script.
    """
    directory = HOME + "/CTL-Flashcards/"
    file_name = "Book_{}_Unit_{}.pdf".format(book, unit)
    try:
        print("Attempting to download " + file_name)
        req = urllib.request.Request("http://kids.liveabc.com/placementtest/flashcards/b{}u{}.pdf".format(book, unit))
        with urllib.request.urlopen(req) as response:
            flashcards = response.read()
            output = open(BASEPATH + file_name, "wb")
            output.write(flashcards)
            return True
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return False
        else:
            print("An error was encountered while downloading " + file_name)
            print("ERROR: " + str(error.code))
            exit()


def check_and_get_cards():
    """
    This function checks the CTL-Flashcards directory for preexisting
    files and runs the download_cards function for any that are not
    present. After completion it reports to the console how many files
    were downloaded and how many did not need to be.
    """
    files_downloaded = 0
    preexisting_files = 0
    for book in range(0, 9): # The Starter book is considered Book 0 officially.
        for unit in range(1, 10):
            file_name = "Book_{}_Unit_{}.pdf".format(book, unit)
            if os.path.isfile(BASEPATH + file_name):
                print(file_name + " already exists. Proceeding to next file.")
                preexisting_files += 1
            elif download_cards(book, unit):
                print("Successfully downloaded " + file_name)
                files_downloaded += 1
            else:
                print("Book {} does not have a Unit {}".format(book, unit))
    print("{} new files were downloaded.".format(files_downloaded))
    print("{} files were already in the directory".format(preexisting_files))


def pdf_to_img(cards_pdf):
    """
    This function takes a multi-page PDF as input, extracts each page as
    a temporary file, creates a JPEG from that file, and finally deletes
    the temporary single-page PDF. This results are stored in the
    CTL-Flashcards/Singles/ directory.
    """
    digits = re.findall("\d", cards_pdf)
    book = digits[-2] # Index from end in case of numbers in $HOME.
    unit = digits[-1] # Index from end in case of numbers in $HOME.
    picNum = 1
    with open(cards_pdf, "rb") as pdfFileObject:
        pdfReader = PyPDF2.PdfFileReader(pdfFileObject, strict=False)
        for pageNum in range(0, pdfReader.numPages, 2):
            outFileName = BASEPATH + "Singles/Book_{0}_Unit_{1}_Word_{2:02d}".format(book, unit, picNum)
            print("Processing Book {0} Unit {1} Word {2:02d}".format(book, unit, picNum))
            pageObject = pdfReader.getPage(pageNum)
            pdfWriter = PyPDF2.PdfFileWriter()
            pdfWriter.addPage(pageObject)
            pdfWriter.removeText()
            pdfWriter.removeLinks()
            with open(outFileName + ".pdf", "wb") as singlePagePdf:
                pdfWriter.write(singlePagePdf)
            with Image(filename = outFileName + ".pdf", resolution = 72) as original:
                original.colorspace = "hsl"
                original.modulate(98, 60, 98) # BSH format.
                original.negate()
                original.format = "jpeg"
                original.crop(width=500, height=450, gravity="center")
                original.compression_quality = 90
                original.save(filename = outFileName + ".jpg")
            picNum += 1
            os.remove(outFileName + ".pdf")


if __name__ == "__main__":
    prepare_directory()
    check_and_get_cards()
    CONVERT = [f for f in os.listdir(BASEPATH) if os.path.isfile(os.path.join(BASEPATH + f))]
    for pdf in CONVERT:
        pdf_to_img(BASEPATH + pdf)
