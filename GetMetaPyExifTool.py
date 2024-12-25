import os
import shutil
from datetime import datetime

from exiftool import ExifToolHelper

sfolderName: str = "C:\\Users\\igsay\\Downloads\\Photos\\sayi"
dfolderName: str = "C:\\Users\\igsay\\Downloads\\Photos"

with ExifToolHelper() as et:
    for d in et.get_tags(
        sfolderName, tags=[]
    ):  # "File:FileName", "File:FileType", "XMP:CreateDate", "EXIF:DateTimeOriginal"
        fName: str = d.get("File:FileName")
        oldFilename = os.path.join(sfolderName, fName)
        tagName: str = ""
        fallBackTagName1: str = "XMP:CreateDate"
        fallBackTagName2: str = "File:FileModifyDate"
        match d.get("File:FileType"):
            case "JPEG":
                tagName = "EXIF:DateTimeOriginal"
            case "PNG":
                tagName = "EXIF:DateTimeOriginal"
            case "HEIC":
                tagName = "EXIF:DateTimeOriginal"
            case "MOV":
                tagName = "QuickTime:CreationDate"
            case "MP4":
                tagName = "QuickTime:CreateDate"
            case "3GP":
                tagName = "QuickTime:CreateDate"
            case "AAE":
                tagName = "PLIST:AdjustmentTimestamp"
            case _:
                tagName = "File:FileName"

        # for k, v in d.items():
        #     print(f"Dict: {k} = {v}")

        dt: str = (
            d.get(tagName)
            if d.get(tagName)
            else d.get(fallBackTagName1)
            if d.get(fallBackTagName1)
            else d.get(fallBackTagName2)
        )
        # if dt is not None or dt == fName:
        #     print(f"Dict: {fName} = {dt}")
        fdate = dt.split(" ")[0]

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

        year = datetime.strptime(fdate, "%Y:%m:%d").strftime("%Y")
        month = datetime.strptime(fdate, "%Y:%m:%d").strftime("%y-%m")

        newFilename = os.path.join(dfolderName, year, month, fName)

        if not os.path.isdir(os.path.join(dfolderName, year)):
            os.mkdir(os.path.join(dfolderName, year))

        if not os.path.isdir(os.path.join(dfolderName, year, month)):
            os.mkdir(os.path.join(dfolderName, year, month))

        shutil.move(oldFilename, newFilename)
        print(f"{fName} move to {newFilename} success\n")
