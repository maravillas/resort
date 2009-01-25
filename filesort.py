#
# The MIT License
#
# Copyright (c) 2009 Matthew Maravillas
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import sys
import os
import shutil
import fnmatch
from datetime import datetime
import exif

use_exif = True
pattern = "*.jpg"

def main(argv):
    if len(argv) < 1:
        usage()
        sys.exit(2)
    
    path = argv[0]
    
    files = fnmatch.filter(os.listdir(path), pattern)
    
    for file in files:
        current_path = os.path.join(path, file)
        
        exif = read_exif(current_path)
        
        if exif:
            date = datetime.strptime(str(exif["Image DateTime"]), "%Y:%m:%d %H:%M:%S")
        
        else:
            date = datetime.datetime.fromtimestamp(os.stat().st_mtime)
        
        new_directory = os.path.join(os.path.split(path)[0],
                                     str(date.year), 
                                     "%02d" % date.month)
        
        print new_directory 
        #os.makedirs(new_directory)
        
        #shutil.move(current_path, os.path.join(new_directory, file))
        
        #shutil.move()

def read_exif(filename):
    try:
        file = open(filename, 'rb')
    except:
        print "%s could not be read" % filename
        return
    
    data = exif.process_file(file)
    
    if not data:
        print "No EXIF information found in %s " % filename
        return
    
    return data
    
        
def usage():
    print "Usage: %s <directory>" % (os.path.basename(sys.argv[0]))
    
if __name__ == "__main__":
    main(sys.argv[1:])
