import urllib.request
import urllib.error
import os

# This will successfully download the files, but I think I can do better.
#
# for book in range(0, 9):
#     for unit in range(1, 10):
#         try:
#             req = urllib.request.Request("http://kids.liveabc.com/placementtest/flashcards/b{}u{}.pdf".format(book, unit))
#             with urllib.request.urlopen(req) as response:
#                 flashcards = response.read()
#                 output = open("Book_{}_Unit_{}.pdf".format(book, unit), "wb")
#                 output.write(flashcards)
#         except urllib.error.HTTPError as error:
#             if error.code == "404":
#                 print("Book {} does not have a Unit {}".format(book, unit))
#                 pass
#             else:
#                 print("ERROR {}".format(error.code))
#                 print(error.read())

HOME = os.path.expanduser("~")

# Check if ~/CTL-Flashcards exists, and create it if it does not.

# Check if a file exists, and create it if it does not.


def get_cards(book, unit):
    """
    This function will attempt to download the corresponding pdf of
    vocabulary cards for a given book and unit. If a 404 error is
    returned, it is assumed that the given book does not have a unit of
    that number. This is printed to the console without exiting the
    script. Other HTML errors will be printed to the console and exit
    the script.
    """
    try:
        req = urllib.request.Request("http://kids.liveabc.com/placementtest/flashcards/b{}u{}.pdf".format(book, unit))
        with urllib.request.urlopen(req) as response:
            flashcards = response.read()
            output = open("Book_{}_Unit_{}.pdf".format(book, unit), "wb")
            output.write(flashcards)
    except urllib.error.HTTPError as error:
        if error.code == 404:
            print("Book {} does not have a Unit {}".format(book, unit))
        else:
            print("ERROR {}".format(error.code))
            exit()


get_cards(5, 99)
get_cards(5, 9)
