import urllib.request
import urllib.error
import os


HOME = os.path.expanduser("~")


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
            print("Something is seriously wrong! ERROR " + error.code)
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
    for book in range(0, 9):
        for unit in range(1, 10):
            file_name = "Book_{}_Unit_{}.pdf".format(book, unit)
            if os.path.isfile(HOME + "/CTL-Flashcards/" + file_name):
                print(file_name + " already exists. Proceeding to next file.")
                preexisting_files += 1
                pass
            elif download_cards(book, unit):
                print("Successfully downloaded " + file_name)
                files_downloaded += 1
            else:
                print("Book {} does not have a Unit {}".format(book, unit))
    print("{} new files were downloaded.".format(files_downloaded))
    print("{} files were already in the directory".format(preexisting_files))


if __name__ == "__main__":
    # Check for and/or create ~/CTL-Flashcards/.
    try:
        if os.path.isdir(HOME + "/CTL-Flashcards/"):
            print("CTL-Flashcards directory exists, proceeding there.")
        else:
            print("CTL-Flashcards directory does not exist, so it will be created.")
            os.mkdir(HOME + "/CTL-Flashcards/")
    except:
        print("Something went wrong while checking for the CTL-Flashcards directory.")
    check_and_get_cards()
