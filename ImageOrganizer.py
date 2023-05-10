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
        self.images = os.listdir(dirname)
        self.dirname = dirname

    def preprocess_exif(self, data):
        data = data.strip()
        data = data.strip("\x00")

        return data

    def show_exif(self):
        for fname in self.images:
            oldFilename = os.path.join(self.dirname, fname)
            with Image.open(oldFilename) as img:
                exif = img._getexif()
                tags = ExifTags.TAGS

                for k, v in exif.items():
                    print("Tag: ", k, "\tValue: ", v, "\tType: ", type(v), "\tTagName: ", tags.get(k))
                print(exif[306])
                print("weadfa")

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
            month = datetime.datetime.strptime(date, "%Y:%m:%d").strftime("%m")

            newFilename = os.path.join(year, month, fname)

            if not os.path.isdir(year):
                os.mkdir(year)

            if not os.path.isdir(os.path.join(year, month)):
                os.mkdir(os.path.join(year, month))

            shutil.copy(oldFilename, newFilename)
            print(f"Image {fname} moved from {oldFilename} to {newFilename} successfully\n")
