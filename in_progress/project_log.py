from __future__ import print_function
import filecmp
from os.path import normpath, basename

file1 = '/Users/filipenegrao/Documents/design-de-tipos/ar_sans_2017/sources_roman/2018-4-23/ar_sans.glyphs'
file2 = '/Users/filipenegrao/Documents/design-de-tipos/ar_sans_2017/sources_roman/2018-04-19/ar_sans.glyphs'
dir2 = '/Users/filipenegrao/Documents/design-de-tipos/ar_sans_2017/sources_roman/2018-4-23'
dir1 = '/Users/filipenegrao/Documents/design-de-tipos/ar_sans_2017/sources_roman/2018-04-19'

print(filecmp.cmp(file1, file2))

from filecmp import dircmp

def print_diff_files(dcmp):

    for name in dcmp.diff_files:
        print("diff_file %s found in %s and %s" % (name, dcmp.left, dcmp.right))

    for sub_dcmp in dcmp.subdirs.values():
        print_diff_files(sub_dcmp)

dcmp = dircmp(dir1, dir2)
print_diff_files(dcmp)

##############


# Open file for reading in text mode (default mode)
f1 = open(file1)
f2 = open(file2)

fname1 = basename(normpath(dir1))
fname2 = basename(normpath(dir2))


# Print confirmation
print("-----------------------------------")
print(("Comparing files ", " > " + fname1, " < " + fname2))
print("-----------------------------------")

# Read the first line from the files
f1_line = f1.readline()
f2_line = f2.readline()

# Initialize counter for line number
line_no = 1

# Loop if either file1 or file2 has not reached EOF
while f1_line != '' or f2_line != '':

    # Strip the leading whitespaces
    f1_line = f1_line.rstrip()
    f2_line = f2_line.rstrip()
    
    # Compare the lines from both file
    if f1_line != f2_line:
        
        # If a line does not exist on file2 then mark the output with + sign
        if f2_line == '' and f1_line != '':
            print((">+", "Line-%d" % line_no, f1_line))
        # otherwise output the line on file1 and mark it with > sign
        elif f1_line != '':
            print((">", "Line-%d" % line_no, f1_line))
            
        # If a line does not exist on file1 then mark the output with + sign
        if f1_line == '' and f2_line != '':
            print(("<+", "Line-%d" % line_no, f2_line))
        # otherwise output the line on file2 and mark it with < sign
        elif f2_line != '':
            print(("<", "Line-%d" %  line_no, f2_line))

        # Print a blank line
        print()

    #Read the next line from the file
    f1_line = f1.readline()
    f2_line = f2.readline()


    #Increment line counter
    line_no += 1

# Close the files
f1.close()
f2.close()

