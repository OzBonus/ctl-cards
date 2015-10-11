import urllib.request
import urllib.error
import os
import PyPDF2
from wand.image import Image


HOME = os.path.expanduser("~")


def prepare_directory():
    try:
        if os.path.isdir(HOME + "/CTL-Flashcards/"):
            print("CTL-Flashcards directory exists, proceeding there.")
        else:
            print("CTL-Flashcards directory does not exist, so it will be created.")
            os.mkdir(HOME + "/CTL-Flashcards/")
            os.mkdir(HOME + "/CTL-Flashcards/Singles/")
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
            output = open(directory + file_name, "wb")
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
            if os.path.isfile(HOME + "/CTL-Flashcards/" + file_name):
                print(file_name + " already exists. Proceeding to next file.")
                preexisting_files += 1
            elif download_cards(book, unit):
                print("Successfully downloaded " + file_name)
                files_downloaded += 1
            else:
                print("Book {} does not have a Unit {}".format(book, unit))
    print("{} new files were downloaded.".format(files_downloaded))
    print("{} files were already in the directory".format(preexisting_files))


def pdf_to_png(book, unit):
    # TODO Try using some filters to make the pictures look less awful.
    # TODO Explore iterating over files in a directory.
    # TODO Refactor this function to work for iteration.
    # TODO Use string searching to extract book and unit number from pdf names.
    picNum = 1
    with open(HOME + "/CTL-Flashcards/Book_1_Unit_1.pdf", "rb") as pdfFileObject:
        # strict = False is required to stop Wand from throwing a critical error.
        pdfReader = PyPDF2.PdfFileReader(pdfFileObject, strict=False)
        for pageNum in range(0, pdfReader.numPages, 2):
            outFileName = "/CTL-Flashcards/Singles/Book_{}_Unit_{}_Word_{}".format(book, unit, picNum)
            pageObject = pdfReader.getPage(pageNum)
            pdfWriter = PyPDF2.PdfFileWriter()
            pdfWriter.addPage(pageObject)
            pdfWriter.removeText()
            pdfWriter.removeLinks()
            with open(HOME + outFileName + ".pdf", "wb") as singlePagePdf:
                pdfWriter.write(singlePagePdf)
            with Image(filename = HOME + outFileName + ".pdf", resolution = 90) as original:
                original.format = "jpeg"
                original.crop(width=500, height=500, gravity="center")
                original.save(filename = HOME + outFileName + ".jpg")
            picNum += 1


if __name__ == "__main__":
    prepare_directory()
    pdf_to_png(4, 6)
