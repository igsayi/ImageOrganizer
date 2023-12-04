# -*- coding: utf-8 -*-
"""

@author: 
"""

import datetime
import os
import shutil

from PIL import ExifTags, Image


class ImageOrganizer:
    def __init__(self, dirname=""):
        self.images = [f for f in os.listdir(dirname) if f.lower().endswith(".jpg")]
        self.images.sort()
        self.dirname = dirname

    def preprocess_exif(self, data):
        data = data.strip()
        data = data.strip("\x00")
        return data

    def show_exif(self):
        for fname in self.images:
            # if fname.lower().endswith(".jpg"):
            oldFilename = os.path.join(self.dirname, fname)
            with Image.open(oldFilename) as img:
                exif: dict = img._getexif()
                print(fname, "-", exif.get(36867))

                # to print all the available tags - refer to the tags.txt file
                # tags = ExifTags.TAGS
                # for k, v in exif.items():
                #    print("Tag: ", k, "\tTagName: ", tags.get(k))  #"\tValue: ", v, "\tType: ", type(v),

    def sort_by_yr_month(self):
        for fname in self.images:

            oldFilename = os.path.join(self.dirname, fname)
            with Image.open(oldFilename) as img:
                exif = img._getexif()

            # manuf = self.preprocess_exif(exif[271])
            # device = self.preprocess_exif(exif[272])
            # exif[306] Date

            ts = self.preprocess_exif(exif[306])
            date = ts.split(" ")[0]

            # %d	Day of the month as a zero-padded decimal.				01, 02, ..., 31
            # %-d	Day of the month as a decimal number.					1, 2, ..., 30
            # %a	Abbreviated weekday name.								Sun, Mon, ...
            # %A	Full weekday name.										Sunday, Monday, ...
            # %b	Abbreviated month name.									Jan, Feb, ..., Dec
            # %B	Full month name.										January, February, ...
            # %m	Month as a zero-padded decimal number.					01, 02, ..., 12
            # %-m	Month as a decimal number.								1, 2, ..., 12
            # %y    Year without century as a zero-padded decimal number.	00, 01, ..., 99
            # %-y   Year without century as a decimal number.				0, 1, ..., 99
            # %Y	Year with century as a decimal number.					2013, 2019 etc.
            # %p	Locale’s AM or PM.										AM, PM

            year = datetime.datetime.strptime(date, "%Y:%m:%d").strftime("%Y")
            month = datetime.datetime.strptime(date, "%Y:%m:%d").strftime("%y-%m")

            newFilename = os.path.join(self.dirname, year, month, fname)

            if not os.path.isdir(os.path.join(self.dirname, year)):
                os.mkdir(os.path.join(self.dirname, year))

            if not os.path.isdir(os.path.join(self.dirname, year, month)):
                os.mkdir(os.path.join(self.dirname, year, month))

            # shutil.move(oldFilename, newFilename)
            print(f"{fname} move from {oldFilename} to {newFilename} success\n")


def main():
    # org = ImageOrganizer("folder")
    org = ImageOrganizer("C:\\Users\\igsay\\Downloads\\Photos")

    # org.sort_by_yr_month()
    org.show_exif()


if __name__ == "__main__":
    main()
