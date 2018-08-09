'''
org.py - image organizer. It will read src_path_to_organize folder for JPG images, sort them by date taken
and save the copy with 0000n_ prefix in the ordered folder under src_path_to_organize.

From command line: python org.py <src_path_to_organize>
'''
import exifread
import fnmatch
import os
import shutil
import sys
from datetime import datetime

def getImageDate(filePath):
    try:
        with open(filePath, 'rb') as fh:
            tags = exifread.process_file(fh, stop_tag="EXIF DateTimeOriginal")
            dateTaken = tags["EXIF DateTimeOriginal"]
            return (filePath, datetime.strptime(str(dateTaken.values), '%Y:%m:%d %H:%M:%S'))
    except Exception as e:
        print(f"{filePath} -> {e}")
        return (filePath, None)

	
def main(path):
	images = []
	
	try:
        files = fnmatch.filter(os.listdir(path), "*.jpg")
        for idx, f in enumerate(files):
            fl, date = getImageDate(f"{path}/{f}")
            print(f"{idx}: {fl} taken at {date}")
            if date != None:
                images.append((fl, date))
    except Exception as e:
        print(e)
    else:
        images.sort(key = lambda t:(t[1], t[0]))
        newdir = f"{path}/ordered"
        os.makedirs(newdir, exist_ok=True)
        for idx, imgData in enumerate(images):
            imgFile, _ = imgData
            _idx = format(idx, '05')
            _newfile = f"{newdir}/{_idx}_{os.path.basename(imgFile)}"
            print(f"{_newfile}")
            shutil.copy2(imgFile, _newfile)

if __name__ == '__main__':
	try:
		path = sys.argv[1]
		main(path)
	except IndexError:
		print "Usage: org.py <src_path_to_organize>"
		sys.exit(1)
    