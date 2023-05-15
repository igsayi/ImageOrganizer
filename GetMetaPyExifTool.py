from exiftool import ExifToolHelper

folderName: str = "H:\\Sridevi-iPhone\\DCIM"

with ExifToolHelper() as et:
    for d in et.get_metadata(folderName):
        fName: str = d.get("File:FileName")
        tagName: str = ""
        fallBackTagName: str = "XMP:CreateDate"
        match d.get("File:FileType"):
            case "JPEG":
                tagName = "EXIF:DateTimeOriginal"
            case "PNG":
                tagName = "EXIF:DateTimeOriginal"
            case "MOV":
                tagName = "QuickTime:CreationDate"
            case "MP4":
                tagName = "QuickTime:CreateDate"
            case "AAE":
                tagName = "PLIST:AdjustmentTimestamp"
            case _:
                tagName = "File:FileName"
                # for k, v in d.items():
                #    print(f"Dict: {k} = {v}")
        dt: str = d.get(tagName) if d.get(tagName) else d.get(fallBackTagName)
        if dt is None or dt == fName:
            print(f"Dict: {fName} = {dt}")
            #for k, v in d.items():
            #    print(f"Dict: {k} = {v}")
